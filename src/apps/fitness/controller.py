from datetime import date, datetime
from typing import Annotated

from fastapi import Depends, Request

from src.apps.fitness.models import Run
from src.config import templates
from src.database import get_conn
from src.dependencies import requires_user
from src.models.user import User

async def index(request: Request, session_user: Annotated[User, Depends(requires_user)]):
    with get_conn() as conn:
        runs = conn.execute(
            "SELECT run_id, user_id, date, distance, units FROM runs WHERE user_id = :user_id ORDER BY date DESC LIMIT 10", 
            {"user_id": session_user.user_id}
            ).fetchall()
    
    runs = [
        Run(
            run_id=run["run_id"],
            user_id=run["user_id"],
            activity_date=date.fromisoformat(run["date"]),
            distance=run["distance"],
            units=run["units"]
        )
        for run in runs
    ]
        
    return templates.TemplateResponse(
        request=request,
        name="fitness/index.html",
        context={
            "session_user": session_user,
            "runs": runs
            }
    )