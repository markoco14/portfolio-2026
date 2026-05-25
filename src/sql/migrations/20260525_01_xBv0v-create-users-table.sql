-- Create users table 
-- depends:

CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    created_at DATETIME DEFAULT (datetime('now')),
    updated_at DATETIME
);


CREATE TRIGGER update_users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = datetime('now') WHERE user_id = OLD.user_id;
END;