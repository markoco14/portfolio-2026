# src/vendor/auth/session.py
import time

from src.models.session import Session


def is_session_expired(session: Session) -> bool:
    if not session:
        return True
    return time.time() > session.expires_at


def is_session_active(session: Session) -> bool:
    if not session:
        return True
    return session.is_active == 1


def is_session_valid(session) -> bool:
    if not session:
        return False
    if is_session_expired(session):
        return False
    if not is_session_active(session):
        return False
    return True
