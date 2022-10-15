from fastapi import FastAPI

from app.api import api



app = FastAPI()

app.include_router(api.router)