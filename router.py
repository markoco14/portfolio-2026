from fastapi import APIRouter

from controllers import public


router = APIRouter()

router.add_api_route("/", public.home, methods=["GET"])


