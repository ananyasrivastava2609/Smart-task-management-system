from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit
from models import db, Task
from extensions import socketio  # Import shared SocketIO instance for real-time updates

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/")
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return render_template("dashboard.html", tasks=tasks)


# ── CREATE ──────────────────────────────────────────────
@tasks_bp.route("/api/tasks", methods=["POST"])
@login_required
def create_task():
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    task = Task(
        title=data["title"],
        description=data.get("description", ""),
        priority=data.get("priority", "Medium"),
        status="Pending",
        user_id=current_user.id,
    )
    db.session.add(task)
    db.session.commit()

    # Broadcast new task to all connected clients of this user
    socketio.emit("task_update", {"action": "created", "task": task.to_dict()})
    return jsonify(task.to_dict()), 201


# ── READ (all tasks) ─────────────────────────────────────
@tasks_bp.route("/api/tasks", methods=["GET"])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])


# ── UPDATE ───────────────────────────────────────────────
@tasks_bp.route("/api/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    data = request.get_json()

    task.title       = data.get("title",       task.title)
    task.description = data.get("description", task.description)
    task.priority    = data.get("priority",    task.priority)
    task.status      = data.get("status",      task.status)

    db.session.commit()
    socketio.emit("task_update", {"action": "updated", "task": task.to_dict()})
    return jsonify(task.to_dict())


# ── DELETE ───────────────────────────────────────────────
@tasks_bp.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    socketio.emit("task_update", {"action": "deleted", "task_id": task_id})
    return jsonify({"message": "Task deleted"})