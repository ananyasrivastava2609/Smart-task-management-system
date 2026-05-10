from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models import Task
import pandas as pd
import numpy as np

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/api/analytics")
@login_required
def get_analytics():
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    if not tasks:
        return jsonify({
            "total": 0, "completed": 0, "pending": 0,
            "completion_pct": 0.0, "by_priority": {}
        })

    # Build DataFrame for Pandas/NumPy processing
    df = pd.DataFrame([t.to_dict() for t in tasks])

    total     = len(df)
    completed = int((df["status"] == "Completed").sum())
    pending   = int((df["status"] == "Pending").sum())

    # NumPy for percentage calculation
    completion_pct = round(float(np.divide(completed, total) * 100), 2)

    # Tasks grouped by priority
    by_priority = df.groupby("priority")["status"].value_counts().to_dict()
    # Convert tuple keys to strings for JSON serialisation
    by_priority = {f"{k[0]}-{k[1]}": int(v) for k, v in by_priority.items()}

    return jsonify({
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_pct": completion_pct,
        "by_priority": by_priority,
    })