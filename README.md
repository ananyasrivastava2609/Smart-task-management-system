# TaskManager — Setup Guide

## Prerequisites
- Python 3.10+
- PostgreSQL 14+

## 1. Clone & Install
```bash
git clone <repo-url>
cd task-manager
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configure Environment
Create a `.env` file in the project root:
SECRET_KEY=your-very-secret-key
DATABASE_URL=postgresql://postgres:password@localhost:5432/taskmanager

## 3. Create the Database
```bash
psql -U postgres -c "CREATE DATABASE taskmanager;"
```
SQLAlchemy will auto-create tables on first run via `db.create_all()`.

## 4. Run
```bash
python app.py
```
Open http://localhost:5000

## Project Structure

```text
task-manager/
│
├── app.py                 # App factory + entry point
├── extensions.py          # Shared SocketIO (breaks circular imports)
├── config.py              # Config from .env
├── models.py              # SQLAlchemy models
│
├── routes/
│   ├── auth.py            # Register / Login / Logout
│   ├── tasks.py           # CRUD REST API + WebSocket emit
│   └── analytics.py       # Pandas/NumPy analytics endpoint
│
├── templates/             # Jinja2 HTML templates
├── static/                # CSS + JavaScript files
│
└── schema.sql             # Raw SQL reference (optional)
```