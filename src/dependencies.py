import sqlite3
from typing import Annotated

from fastapi import Depends, Request

from src import session_repository, user_repository
from src.database import get_conn
from src.vendor.auth.session import is_session_valid


def requires_user(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_conn)]):
    session_token = request.cookies.get("session")

    if not session_token:
        return None

    try:
        session = session_repository.get_by_token(conn=conn, token=session_token)
    except Exception:
        return None

    if not is_session_valid(session=session):
        return None
    
    try:
        user = user_repository.get(conn=conn, user_id=session.user_id)
    except Exception:
        return None
    
    return user

    