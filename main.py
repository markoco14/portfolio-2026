from fastapi import FastAPI

from src.portfolio.router import router
from src.apps.fitness.router import fitness_router
from src.demos.router import demo_router

app = FastAPI()
app.include_router(router=router)
app.include_router(router=fitness_router)
app.include_router(router=demo_router)


