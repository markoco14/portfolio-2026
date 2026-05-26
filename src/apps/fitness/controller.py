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

async def new(
        request: Request, 
        session_user: Annotated[User, Depends(requires_user)]
        ):
    return templates.TemplateResponse(
        request=request,
        name="fitness/new.html",
        context={
            "session_user": session_user,
        }
    )

def parse_distance(value: str) -> float | None:
    try:
        distance = float(value)
        if distance <= 0:
            return None
        return distance
    except (ValueError, TypeError):
        return None

async def save(
        request: Request, 
        session_user: Annotated[User, Depends(requires_user)]
        ):
    form_data = await request.form()
    form_distance = parse_distance(form_data.get("distance"))
    form_date = form_data.get("activity_date")

    if not form_distance:
        return "Invalid distance"

    with get_conn() as conn:
        conn.execute(
            "INSERT INTO runs (user_id, date, distance, units) VALUES (:user_id, :date, :distance, :units);",
            {"user_id": session_user.user_id, "date": form_date, "distance": form_distance, "units": "km"})
        conn.commit()

    return "OK"