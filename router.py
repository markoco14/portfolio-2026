from fastapi import APIRouter

from controllers import public


router = APIRouter()

router.add_api_route("/", public.home, methods=["GET"])

router.add_api_route("/demos/compass/scheduleboard", public.schedule_board, methods=["GET"])

