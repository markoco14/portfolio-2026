import sqlite3

from src.models.user import User


def get(conn: sqlite3.Connection, user_id: int):
    row = conn.execute(
        "SELECT user_id, email FROM users WHERE user_id = :user_id", 
        {"user_id": user_id}
        ).fetchone()
    
    if not row:
        return None
    
    return User(
        user_id=row["user_id"],
        email=row["email"]
        )
