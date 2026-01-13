from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

async def home(request: Request):
    return HTMLResponse(status_code=200, content="<p>Hello world</p>")

router = APIRouter()

router.add_api_route("/", home, methods=["GET"])

app.include_router(router=router)


