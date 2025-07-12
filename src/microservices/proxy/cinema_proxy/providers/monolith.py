import os
import json 

import httpx

MONOLITH_URL = os.environ.get("MONOLITH_URL")


async def list_movies():
    async with httpx.AsyncClient() as client:
        response = await client.get(url=MONOLITH_URL + "/api/movies")
        return json.loads(response.text)


async def list_users():
    async with httpx.AsyncClient() as client:
        response = await client.get(url=MONOLITH_URL + "/api/users")
        return json.loads(response.text)
