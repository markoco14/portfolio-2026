from fastapi import Request

from src.database import get_conn
from src.models.session import Session
from src.models.user import User
from src.vendor.auth.session import is_session_valid


def requires_user(request: Request):
    session_token = request.cookies.get("session")

    if not session_token:
        return None
    
    with get_conn() as conn:
        session_row = conn.execute(
            "SELECT session_id, user_id, token, is_active, expires_at, revoked_at FROM sessions WHERE token = :token", 
            {"token": session_token}
            ).fetchone()
        session = Session(**session_row)

    if not session:
        return None
    
    if not is_session_valid(session=session):
        return None
    
    with get_conn() as conn:
        user_row = conn.execute(
            "SELECT user_id, email FROM users WHERE user_id = :user_id", 
            {"user_id": session.user_id}
            ).fetchone()
        user = User(**user_row)

    if not user:
        return None
    
    return user

    