from fastapi import Request

from config import templates

async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

async def schedule_board(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="schedule-board.html",
        context={}
    )