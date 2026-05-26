from fastapi import Request

from src.config import templates

async def index(request: Request):
    session_user = request.cookies.get("session")
    return templates.TemplateResponse(
        request=request,
        name="fitness/index.html",
        context={
            "session_user": session_user
            }
    )