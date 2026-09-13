from datetime import date
import sqlite3
from types import SimpleNamespace
from typing import Annotated

from fastapi import Depends, Request, Response

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

    try:
        strength_log_rows = conn.execute("SELECT * FROM strength_log JOIN exercise USING (exercise_id);").fetchall()
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="fitness/index.html",
            context={
                "session_user": session_user,
                "runs": []
                }
        )

    strength_log = [dict(entry) for entry in strength_log_rows]
    for entry in strength_log:
        if entry["activity_date"]:
            entry["activity_date"] = date.fromisoformat(entry["activity_date"])
        
    return templates.TemplateResponse(
        request=request,
        name="fitness/index.html",
        context={
            "session_user": session_user,
            "runs": runs,
            "strength_log": strength_log
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

async def new_strength(
        request: Request, 
        session_user: Annotated[User, Depends(requires_user)],
        conn: Annotated[sqlite3.Connection, Depends(get_conn)]
        ):
    if not session_user:
        return "Can't do that"

    try:
        exercise_rows = conn.execute("SELECT * FROM exercise;").fetchall()
    except Exception as e:
        return Response(status_code=500, content="Something went wrong on our end, please refresh.")


    
    return templates.TemplateResponse(
        request=request,
        name="fitness/strength/new.html",
        context={
            "session_user": session_user,
            "exercises": exercise_rows
            }
    )

async def save_strength(
        request: Request, 
        session_user: Annotated[User, Depends(requires_user)],
        conn: Annotated[sqlite3.Connection, Depends(get_conn)]
        ):
    if not session_user:
        return "Can't do that"
    form_data = await request.form()

    exercise = form_data.get("exercise", "").strip()
    if not exercise:
        return Response(status_code=422, content="You need to choose an exericse")


    reps = form_data.get("reps", "").strip()
    if not reps:
        return Response(status_code=422, content="You need to choose how many reps")

    activity_date = form_data.get("activity_date", "").strip()

    details = form_data.get("details", "").strip()

    if details == "weighted":
        units = form_data.get("units", "").strip()
        weight = form_data.get("weight", "").strip()
        if not units or not weight:
            return Response(status_code=422, content="You need units and weight")
        try:
            conn.execute(
                """
                INSERT INTO strength_log (
                    exercise_id, activity_date, reps, units, weight
                ) VALUES (
                    :exercise_id, :activity_date, :reps, :units, :weight
                );
                """,
                {
                    "exercise_id": exercise,
                    "reps": reps,
                    "activity_date": activity_date,
                    "units": units,
                    "weight": weight
                }
                )
            conn.commit()
        except Exception as e:
            return Response(status_code=500, content="Something went wrong, please refresh and try again")
        return "ok"
    elif details == "assisted":
        band = form_data.get("band", "").strip()
        if not band:
            return Response(status_code=422, content="You need a band")
        try:
            conn.execute(
                """
                INSERT INTO strength_log (
                    exercise_id, activity_date, reps, band
                ) VALUES (
                    :exercise_id, :activity_date, :reps, :band
                );
                """,
                {
                    "exercise_id": exercise,
                    "reps": reps,
                    "activity_date": activity_date,
                    "band": band
                }
                )
            conn.commit()
        except Exception as e:
            return Response(status_code=500, content="Something went wrong, please refresh and try again")

        return "ok"

    try:
        conn.execute(
            """
            INSERT INTO strength_log (
                exercise_id, activity_date, reps
            ) VALUES (
                :exercise_id, :activity_date, :reps
            );
            """,
            {
                "exercise_id": exercise,
                "reps": reps,
                "activity_date": activity_date
            }
            )
        conn.commit()
    except Exception as e:
        return Response(status_code=500, content="Something went wrong, please refresh and try again")
    
    return "OK"


async def inputs(request: Request):
    details = request.query_params.get("details")
    return templates.TemplateResponse(
        request=request,
        name="fitness/strength/_inputs.html",
        context={
            "details": details
        }
    )
