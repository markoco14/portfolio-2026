import asyncio

from fastapi import Request

from config import templates

async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

async def schedule_board(request: Request):

    query_params = request.query_params
    date = query_params.get("date")

    if not date:
        date = "2026-05-10"

    await asyncio.sleep(0.5)
    
    students_only = query_params.get("students_only")
    if students_only:
        students = [1, 2, 3, 4]
        return templates.TemplateResponse(
            request=request,
            name="_students.html",
            context={
                "students": students
            }
        )


    return templates.TemplateResponse(
        request=request,
        name="schedule-board.html",
        context={
            "date": date
        }
    )