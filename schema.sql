-- Run once to create the database (optional if using SQLAlchemy init)
CREATE DATABASE taskmanager;

-- SQLAlchemy will auto-create tables via db.create_all()
-- But if you prefer raw SQL:

CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    username    VARCHAR(80)  UNIQUE NOT NULL,
    email       VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tasks (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    priority    VARCHAR(10)  NOT NULL DEFAULT 'Medium',
    status      VARCHAR(10)  NOT NULL DEFAULT 'Pending',
    created_at  TIMESTAMP DEFAULT NOW(),
    user_id     INTEGER REFERENCES users(id) ON DELETE CASCADE
);