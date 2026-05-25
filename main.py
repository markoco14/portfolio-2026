from fastapi import FastAPI

from router import router
from apps.fitness.router import fitness_router

app = FastAPI()
app.include_router(router=router)
app.include_router(router=fitness_router)


