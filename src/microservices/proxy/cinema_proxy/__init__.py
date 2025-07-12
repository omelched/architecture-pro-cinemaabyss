import os
import random
from typing import Optional

from fastapi import FastAPI, Response, Request
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
async def list_movies(id: Optional[str] = None):
    if id is None:
        if is_routed_to_microservice():
            movie_list = await monolith.list_movies()
        else:
            movie_list = await movies.list_movies()

        return JSONResponse(movie_list)
    else:
        if is_routed_to_microservice():
            found_movie = await monolith.get_movie(id)
        else:
            found_movie = await movies.get_movie(id)

        return JSONResponse(found_movie)


@app.post("/api/movies/")
async def create_movie(request: Request):
    if is_routed_to_microservice():
        created_movie = await monolith.create_movie(await request.json())
    else:
        created_movie = await movies.create_movie(await request.json())

    return JSONResponse(created_movie, status_code=201)


@app.get("/api/users/")
async def list_users(id: Optional[str] = None):
    if id is None:
        return JSONResponse(await monolith.list_users())
    else:
        return JSONResponse(await monolith.get_user(id))


@app.post("/api/users/")
async def create_user(request: Request):
    return JSONResponse(
        await monolith.create_user(await request.json()), status_code=201
    )
