import os
import random

from fastapi import FastAPI, Response
from starlette.responses import JSONResponse

from .providers import monolith, movies

app = FastAPI()

MOVIES_MIGRATION_PERCENT = os.environ.get("MOVIES_MIGRATION_PERCENT")


@app.get("/health/")
async def health_check():
    return Response()


@app.get("/api/movies/")
async def list_movies():
    is_routed_to_microservice = random.randint(0, 99) < int(MOVIES_MIGRATION_PERCENT)

    if is_routed_to_microservice:
        movie_list = await monolith.list_movies()
    else:
        movie_list = await movies.list_movies()

    return JSONResponse(movie_list)


@app.get("/api/users/")
async def list_users():
    return JSONResponse(await monolith.list_users())