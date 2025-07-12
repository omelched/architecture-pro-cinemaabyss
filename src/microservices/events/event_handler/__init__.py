import asyncio
import json

from fastapi import FastAPI, Request, Response
from starlette.responses import JSONResponse

from .consumer import consume
from .producer import produce

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume())


@app.get("/api/events/health")
async def health():
    return JSONResponse({"status": True})


@app.post("/api/events/movie")
async def product_movie(request: Request):
    await produce("movie", json.dumps(await request.json()))
    return JSONResponse({"status": "success"}, status_code=201)


@app.post("/api/events/user")
async def product_user(request: Request):
    await produce("user", json.dumps(await request.json()))
    return JSONResponse({"status": "success"}, status_code=201)


@app.post("/api/events/payment")
async def product_payments(request: Request):
    await produce("payment", json.dumps(await request.json()))
    return JSONResponse({"status": "success"}, status_code=201)
