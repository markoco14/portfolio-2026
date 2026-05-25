-- Create runs table
-- depends: 

CREATE TABLE IF NOT EXISTS runs(
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    distance REAL NOT NULL,
    units TEXT NOT NULL DEFAULT 'km' CHECK(units IN ('km', 'mi')),
    notes TEXT,
    created_at DATETIME DEFAULT (datetime('now')),
    updated_at DATETIME
);

CREATE TRIGGER update_runs_updated_at
AFTER UPDATE ON runs
FOR EACH ROW
BEGIN
    UPDATE runs SET updated_at = datetime('now') WHERE run_id = OLD.run_id;
END;