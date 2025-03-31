from fastapi import FastAPI

from src.audio.controller import router as audio_router
from src.users.controller import router as users_router


def register_routes(app: FastAPI):
    app.include_router(users_router)
    app.include_router(audio_router)
