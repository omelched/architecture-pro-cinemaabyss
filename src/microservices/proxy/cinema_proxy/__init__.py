import os
import random

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
async def list_movies():
    if is_routed_to_microservice():
        movie_list = await monolith.list_movies()
    else:
        movie_list = await movies.list_movies()

    return JSONResponse(movie_list)


@app.post("/api/movies/")
async def create_movie(request: Request):
    if is_routed_to_microservice():
        created_movie = await monolith.create_movie(await request.json())
    else:
        created_movie = await movies.create_movie(await request.json())

    return JSONResponse(created_movie, status_code=201)


@app.get("/api/movies/")
async def get_movie(id: str):
    if is_routed_to_microservice():
        found_movie = await monolith.get_movie(id)
    else:
        found_movie = await movies.get_movie(id)

    return JSONResponse(found_movie)


@app.get("/api/users/")
async def list_users():
    return JSONResponse(await monolith.list_users())


@app.post("/api/users/")
async def create_user(request: Request):
    return JSONResponse(
        await monolith.create_user(await request.json()), status_code=201
    )


@app.get("/api/users/")
async def get_user(id: str):
    return JSONResponse(await monolith.get_user(id))
