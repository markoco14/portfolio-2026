CREATE TABLE runs(
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    distance REAL NOT NULL,
    units TEXT NOT NULL DEFAULT 'km' CHECK(units IN ('km', 'mi')),
    notes TEXT,
    created_at DATETIME DEFAULT (datetime('now')),
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
CREATE TRIGGER update_runs_updated_at
AFTER UPDATE ON runs
FOR EACH ROW
BEGIN
    UPDATE runs SET updated_at = datetime('now') WHERE run_id = OLD.run_id;
END;
