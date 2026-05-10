import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")

    # PostgreSQL connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/taskmanager"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SocketIO
    SOCKETIO_ASYNC_MODE = "eventlet"