-- Create sessions table 
-- depends: 20260525_01_xBv0v-create-users-table

CREATE TABLE IF NOT EXISTS sessions(
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT (datetime('now')),
    expires_at DATETIME NOT NULL,
    revoked_at DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TRIGGER set_revoked_at
AFTER UPDATE OF is_active ON sessions
FOR EACH ROW
WHEN NEW.is_active = 0 AND OLD.is_active = 1
BEGIN
    UPDATE sessions SET revoked_at = datetime('now') WHERE session_id = OLD.session_id;
END;
