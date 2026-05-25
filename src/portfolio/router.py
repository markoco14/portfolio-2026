from fastapi import APIRouter

from src.portfolio import controller


router = APIRouter()

router.add_api_route("/", controller.home, methods=["GET"])
router.add_api_route("/signin", controller.signin, methods=["POST"])

