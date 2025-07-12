import os
import json 

import httpx

MONOLITH_URL = os.environ.get("MONOLITH_URL")


async def list_movies():
    async with httpx.AsyncClient() as client:
        response = await client.get(url=MONOLITH_URL + "/api/movies")
        return json.loads(response.text)


async def create_movie(data):
    async with httpx.AsyncClient() as client:
        response = await client.post(url=MONOLITH_URL + "/api/movies", json=data)
        return json.loads(response.text)

async def get_movie(id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url=MONOLITH_URL + "/api/movies" + f"?id={id}")
        return json.loads(response.text)


async def list_users():
    async with httpx.AsyncClient() as client:
        response = await client.get(url=MONOLITH_URL + "/api/users")
        return json.loads(response.text)

async def create_user(data):
    async with httpx.AsyncClient() as client:
        response = await client.post(url=MONOLITH_URL + "/api/users", json=data)
        return json.loads(response.text)

async def get_user(id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url=MONOLITH_URL + "/api/users" + f"?id={id}")
        return json.loads(response.text)
