import asyncio
from datetime import date

from fastapi import Request

from src.config import templates

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

        classes_students = [
            {"class_id": 1, "students": [1, 2, 3, 4, 5, 6]},
            {"class_id": 2, "students": [1, 2]},
            {"class_id": 3, "students": [1, 2, 3]},
            ]

        return templates.TemplateResponse(
            request=request,
            name="_students.html",
            context={
                "classes_students": classes_students,
            }
        )
    
    date_iso_calendar = selected_date.isocalendar()
    year_week_number = date_iso_calendar.week

    quick_date_buttons = []
    for i in range(1, 7):
        quick_date_buttons.append(date.fromisocalendar(selected_date.year, year_week_number, i))

    classes = [(1, "9:30"), (2, "10:30"), (3, "11:30")]
    class_query_string = ""
    for row in classes:
        class_query_string += f"&class={row[0]}"
        class_query_string = class_query_string.lstrip("&")

    return templates.TemplateResponse(
        request=request,
        name="schedule-board.html",
        context={
            "selected_date": selected_date.strftime("%Y-%m-%d"),
            "header_date": selected_date.strftime("%A %B %d, %Y"),
            "quick_date_buttons": quick_date_buttons,
            "speed": speed,
            "classes": classes,
            "class_query_string": class_query_string
        }
    )