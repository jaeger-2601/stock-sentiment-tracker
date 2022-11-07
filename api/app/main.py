from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api

origins = [
    'http://localhost:8000',
    'http://localhost:3000'
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api.router)
