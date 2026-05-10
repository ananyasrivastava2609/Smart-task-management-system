import eventlet
eventlet.monkey_patch()   # Must be first — patches stdlib for async I/O

from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, bcrypt, User
from extensions import socketio  # Shared SocketIO instance for real-time updates

# ── Shared SocketIO instance (imported by routes/tasks.py) ──
#socketio = SocketIO()

# Expose socketio via a tiny extensions module so routes can import it
import extensions  # noqa: E402 – populated below


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app, async_mode="eventlet", cors_allowed_origins="*")

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth      import auth_bp
    from routes.tasks     import tasks_bp
    from routes.analytics import analytics_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(analytics_bp)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)