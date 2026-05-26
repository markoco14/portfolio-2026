import sqlite3
from typing import Annotated

from fastapi import Depends, Request

from src.config import templates
from src.database import get_conn
from src.dependencies import requires_user
from src.models.user import User

async def index(request: Request, session_user: Annotated[User, Depends(requires_user)]):
    with get_conn() as conn:
        runs = conn.execute(
            "SELECT * FROM runs WHERE user_id = :user_id ORDER BY date DESC LIMIT 10", 
            {"user_id": session_user.user_id}
            ).fetchall()
        
    return templates.TemplateResponse(
        request=request,
        name="fitness/index.html",
        context={
            "session_user": session_user,
            "runs": runs
            }
    )