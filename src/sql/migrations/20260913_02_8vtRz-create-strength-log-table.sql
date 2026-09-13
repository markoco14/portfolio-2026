-- Create strength log table 
-- depends: 20260913_01_af0E5-create-exercises-table

CREATE TABLE strength_log(
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_id INTEGER NOT NULL,
    activity_date DATE NOT NULL,
    reps INTEGER NOT NULL,
    side TEXT CHECK (side IN ("left", "right")) DEFAULT NULL,
    units TEXT,
    weight REAL,
    band TEXT CHECK (band IN ("red")) DEFAULT NULL,
    created_at DATETIME DEFAULT (datetime('now')),
    updated_at DATETIME
);