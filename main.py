from fastapi import APIRouter, FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

router = APIRouter()

router.add_api_route("/", home, methods=["GET"])

app.include_router(router=router)


