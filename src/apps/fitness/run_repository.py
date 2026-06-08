from datetime import date
import sqlite3
from typing import List

from src.apps.fitness.models import Run


def list(conn: sqlite3.Connection, user_id: int) -> List[Run]:
    rows = conn.execute(
            """
            SELECT 
                run_id, 
                user_id, 
                date, 
                distance, 
                units 
            FROM runs 
            WHERE user_id = :user_id 
            ORDER BY date DESC 
            LIMIT 10
            """, 
            {"user_id": user_id}
            ).fetchall()
    
    if not rows:
        return []
    
    runs = [
        Run(
            run_id=row["run_id"],
            user_id=row["user_id"],
            activity_date=row["date"],
            distance=row["distance"],
            units=row["units"]
        )
        for row in rows
    ]

    return runs


def save(conn: sqlite3.Connection, user_id: int, date: date, distance: float):
    conn.execute(
        "INSERT INTO runs (user_id, date, distance, units) VALUES (:user_id, :date, :distance, :units);",
        {"user_id": user_id, "date": date, "distance": distance, "units": "km"})
    conn.commit()