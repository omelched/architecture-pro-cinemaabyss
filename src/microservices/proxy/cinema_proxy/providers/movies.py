import os
import json

import httpx

MOVIES_SERVICE_URL = os.environ.get("MOVIES_SERVICE_URL")


async def list_movies():
    async with httpx.AsyncClient() as client:
        response = await client.get(url=MOVIES_SERVICE_URL + "/api/movies")
        return json.loads(response.text)


async def create_movie(data):
    async with httpx.AsyncClient() as client:
        response = await client.post(url=MOVIES_SERVICE_URL + "/api/movies", json=data)
        return json.loads(response.text)


async def get_movie(id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url=MOVIES_SERVICE_URL + "/api/movies" + "?id={id}")
        return json.loads(response.text)
