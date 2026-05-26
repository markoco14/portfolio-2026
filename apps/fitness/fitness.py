from fastapi import Request

from src.config import templates

def index(request: Request):
    user = request.cookies.get("session")
    return templates.TemplateResponse(
        request=request,
        name="fitness/index.html",
        context={
            "session_user": user
            }
    )