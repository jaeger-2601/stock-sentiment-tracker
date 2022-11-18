import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_redis_cache import FastApiRedisCache, cache

from dotenv import load_dotenv

from app.api import api

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

    redis_cache = FastApiRedisCache()
    redis_cache.init(host_url=os.environ["REDIS_URL"], prefix="api-cache")
