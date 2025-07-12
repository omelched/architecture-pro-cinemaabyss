import os
import random

from fastapi import FastAPI, Response
from starlette.responses import JSONResponse

from .providers import monolith, movies

app = FastAPI()

GRADUAL_MIGRATION = os.environ.get("GRADUAL_MIGRATION")
MOVIES_MIGRATION_PERCENT = os.environ.get("MOVIES_MIGRATION_PERCENT")


def is_routed_to_microservice() -> bool:
    if not GRADUAL_MIGRATION == "true":
        return True

    return random.randint(0, 99) < int(MOVIES_MIGRATION_PERCENT)


@app.get("/health/")
async def health_check():
    return Response()


@app.get("/api/movies/")
async def list_movies():
    if is_routed_to_microservice():
        movie_list = await monolith.list_movies()
    else:
        movie_list = await movies.list_movies()

    return JSONResponse(movie_list)


@app.get("/api/users/")
async def list_users():
    return JSONResponse(await monolith.list_users())
