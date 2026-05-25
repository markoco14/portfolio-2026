from fastapi import FastAPI

from src.router import router
from src.apps.fitness.router import fitness_router

app = FastAPI()
app.include_router(router=router)
app.include_router(router=fitness_router)


