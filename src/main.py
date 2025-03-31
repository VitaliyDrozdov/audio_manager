from fastapi import FastAPI

from src.logging_ import LogLevels, configure_logging
from src.routes import register_routes

app = FastAPI(title="audio_manager", summary="API_v1")


register_routes(app)
configure_logging(LogLevels.debug)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8100)
