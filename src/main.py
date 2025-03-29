from fastapi import FastAPI


app = FastAPI(title="audio_manager", summary="API_v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main.app", reload=True, port=8000)
