from fastapi import APIRouter

from src.apps.fitness import controller


fitness_router = APIRouter()

fitness_router.add_api_route("/fitness", controller.index, methods=["GET"])
fitness_router.add_api_route("/fitness/new", controller.new, methods=["GET"])
fitness_router.add_api_route("/fitness", controller.save, methods=["POST"])