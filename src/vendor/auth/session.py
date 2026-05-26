# src/vendor/auth/session.py
import time


def is_session_expired(session) -> bool:
    if not session:
        return True
    return time.time() > session["expires_at"]


def is_session_valid(session) -> bool:
    if not session:
        return False
    return not is_session_expired(session)