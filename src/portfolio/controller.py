from fastapi import Request, Response

from src.database import get_conn
from src.config import templates
from src.vendor.auth.crypto import verify_password
from src.vendor.auth.validators import is_valid_email


async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


async def signin(request: Request):
    form_data = await request.form()

    email = form_data.get("username", "").strip()
    password = form_data.get("password", "").strip()

    if not email or not password:
        return templates.TemplateResponse(
            request=request,
            name="_form_response.html",
            status_code=422,
            context={
                "unprocessable_error": "Something is wrong with your email or password",
                "email_error": "",
                "password_error": ""
            }
        )
    
    email_error = ""
    user = None
    if not is_valid_email(email=email):
        email_error = "Invalid email"
    else:
        with get_conn() as conn:
            user = conn.execute(
                "SELECT user_id, email, hashed_password FROM users WHERE email = :email",
                {"email": email}
                ).fetchone()
        if not user:
            email_error = "Invalid email"
    
    password_error = ""
    if user and not verify_password(password=password, hashed=user["hashed_password"]):
        password_error = "Invalid password"

    if email_error or password_error:
        return templates.TemplateResponse(
            request=request,
            name="_form_response.html",
            context={
                "unprocessable_error": "",
                "email_error": email_error,
                "password_error": password_error
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="_form_response.html",
        context={
            "unprocessable_error": "",
            "email_error": "",
            "password_error": ""
        },
        headers={
            "hx-refresh": "true"
        }
    )