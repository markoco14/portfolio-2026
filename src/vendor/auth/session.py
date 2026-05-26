# src/vendor/auth/session.py
from datetime import datetime


def is_session_expired(session) -> bool:
    if not session:
        return True
    expires_at = datetime.fromisoformat(session["expires_at"])
    return datetime.utcnow() > expires_at


def is_session_valid(session) -> bool:
    if not session:
        return False
    return not is_session_expired(session)