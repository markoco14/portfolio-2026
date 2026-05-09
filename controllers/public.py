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

    return templates.TemplateResponse(
        request=request,
        name="schedule-board.html",
        context={
            "date": date
        }
    )