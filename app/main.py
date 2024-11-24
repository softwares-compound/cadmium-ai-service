from fastapi import FastAPI
from app.api.endpoints import logs

app = FastAPI()

app.include_router(logs.router, prefix="/logs", tags=["logs"])
