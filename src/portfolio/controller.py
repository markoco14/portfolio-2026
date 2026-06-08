import sqlite3
import time
from typing import Annotated
import uuid

from fastapi import Depends, Request

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


async def signin(
        request: Request,
        conn: Annotated[sqlite3.Connection, Depends(get_conn)]
        ):
    form_data = await request.form()

    email = form_data.get("username", "").strip()
    password = form_data.get("password", "").strip()

    if not email or not password:
        return templates.TemplateResponse(
            request=request,
            name="_form_response.html",
            status_code=422,
            context={
                "general_error": "Something is wrong with your email or password",
                "email_error": "",
                "password_error": ""
            }
        )
    
    email_error = ""
    user = None
    if not is_valid_email(email=email):
        email_error = "Invalid email"
    else:
        try:
            user = conn.execute(
                "SELECT user_id, email, hashed_password FROM users WHERE email = :email",
                {"email": email}
                ).fetchone()
            
            if not user:
                email_error = "Invalid email"
        except Exception as e:
            return "Server error, please try again"
    
    password_error = ""
    if user and not verify_password(password=password, hashed=user["hashed_password"]):
        password_error = "Invalid password"

    if email_error or password_error:
        return templates.TemplateResponse(
            request=request,
            name="_form_response.html",
            context={
                "general_error": "",
                "email_error": email_error,
                "password_error": password_error
            }
        )
    
    token = str(uuid.uuid4())
    expires_at = int(time.time()) + (60 * 60 * 24 * 3)
    try:
        conn.execute(
            "INSERT INTO sessions (user_id, token, expires_at) VALUES (:user_id, :token, :expires_at);",
            { "user_id": user["user_id"], "token": token, "expires_at": expires_at })
        conn.commit()
    except Exception as e:
        return "Server error, please try again"
    
    response = templates.TemplateResponse(
        request=request,
        name="_form_response.html",
        context={
            "general_error": "",
            "email_error": "",
            "password_error": ""
        },
        headers={
            "hx-refresh": "true"
        }
    )

    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=(60 * 60 * 24 * 3)
    )

    return response