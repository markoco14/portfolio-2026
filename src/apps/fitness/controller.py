from datetime import date
import sqlite3
from typing import Annotated

from fastapi import Depends, Request

from src.apps.fitness import run_repository
from src.config import templates
from src.database import get_conn
from src.dependencies import requires_user
from src.models.user import User

async def index(
        request: Request, 
        session_user: Annotated[User, Depends(requires_user)], 
        conn: Annotated[sqlite3.Connection, Depends(get_conn)]
        ):
    if not session_user:
        return templates.TemplateResponse(
            request=request,
            name="fitness/index.html",
            context={
                "session_user": None,
                "runs": []
                }
        )

    try:
        runs = run_repository.list(conn=conn, user_id=session_user.user_id)
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="fitness/index.html",
            context={
                "session_user": session_user,
                "runs": []
                }
        )
    
    for run in runs:
        if run.activity_date:
            run.activity_date = date.fromisoformat(run.activity_date)
        
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
        session_user: Annotated[User, Depends(requires_user)],
        conn: Annotated[sqlite3.Connection, Depends(get_conn)]
        ):
    form_data = await request.form()
    form_distance = parse_distance(form_data.get("distance"))
    form_date = form_data.get("activity_date")

    if not form_distance:
        return "Invalid distance"

    try:
        run_repository.save(
            conn=conn, 
            user_id=session_user.user_id, 
            date=form_date, 
            distance=form_distance
            )
    except Exception as e:
        return "Error saving run, please try again."

    return "OK"