import asyncio
from datetime import date

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
    selected_date = query_params.get("selected_date")
    try:
        speed = float(query_params.get("speed", 0.5))
    except (ValueError, TypeError):
        speed = 0.5

    speed = max(0, min(speed, 10))

    if not selected_date:
        selected_date = date.today()
    else:
        selected_date = date.fromisoformat(selected_date)


    await asyncio.sleep(0.2)
    
    students_only = query_params.get("students_only")
    if students_only:
        await asyncio.sleep(speed)

        students = [1, 2, 3, 4]

        return templates.TemplateResponse(
            request=request,
            name="_students.html",
            context={
                "students": students
            }
        )
    
    date_iso_calendar = selected_date.isocalendar()
    year_week_number = date_iso_calendar.week

    quick_date_buttons = []
    for i in range(1, 7):
        quick_date_buttons.append(date.fromisocalendar(selected_date.year, year_week_number, i))

    return templates.TemplateResponse(
        request=request,
        name="schedule-board.html",
        context={
            "selected_date": selected_date.strftime("%Y-%m-%d"),
            "header_date": selected_date.strftime("%A %B %d, %Y"),
            "quick_date_buttons": quick_date_buttons,
            "speed": speed
        }
    )