from fastapi import FastAPI

from src.audio.controller import router as audio_router
from src.auth.controller import router as auth_router
from src.users.controller import router as users_router


def register_routes(app: FastAPI):
    """Registers all routers in the FastAPI application."""
    app.include_router(auth_router)
    app.include_router(audio_router)
    app.include_router(users_router)
