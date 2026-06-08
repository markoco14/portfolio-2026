import sqlite3

from src.models.session import Session


def get_by_token(conn: sqlite3.Connection, token: str):
    row = conn.execute(
        "SELECT session_id, user_id, token, is_active, expires_at, revoked_at FROM sessions WHERE token = :token", 
        {"token": token}
        ).fetchone()

    if not row:
        return None
    
    return Session(
        session_id=row["session_id"],
        user_id=row["user_id"],
        token=row["token"],
        is_active=row["is_active"],
        expires_at=row["expires_at"]
        )

