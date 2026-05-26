from fastapi import APIRouter

from src.demos import controller


demo_router = APIRouter()

demo_router.add_api_route("/demos/compass/scheduleboard", controller.schedule_board, methods=["GET"])

