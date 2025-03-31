from fastapi import FastAPI

from src.logging import LogLevels, configure_logging
from src.routes import register_routes

app = FastAPI(title="audio_manager", summary="API_v1")


register_routes(app)
configure_logging(LogLevels.info)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8100)
