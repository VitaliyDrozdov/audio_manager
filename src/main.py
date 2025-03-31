from fastapi import FastAPI

from src.routes import register_routes

app = FastAPI(title="audio_manager", summary="API_v1")


register_routes(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8110)
    register_routes(app)
