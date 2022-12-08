import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from dotenv import load_dotenv

from .api import api

origins = ["http://localhost:8000", "http://localhost:3000"]

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api.router)


@app.on_event("startup")
def startup():

    redis = aioredis.from_url(
        os.environ["REDIS_URL"], encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="api-cache")
