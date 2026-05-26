from fastapi import Request

from src.database import get_conn
from src.vendor.auth.session import is_session_expired


def requires_user(request: Request):
    session_token = request.cookies.get("session")

    if not session_token:
        return None
    
    with get_conn() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE token = :token", {"token": session_token}).fetchone()

    if not session:
        return None
    
    if is_session_expired(session=session):
        return None
    
    with get_conn() as conn:
        user = conn.execute("SELECT user_id, email FROM users WHERE user_id = :user_id", {"user_id": session["user_id"]}).fetchone()

    if not user:
        return None
    
    return user

    