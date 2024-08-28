import uvicorn
from backend.api.routers.router import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

HOST: str = "0.0.0.0"
PORT: int = 5000


def get_app() -> FastAPI:
    """
    FastAPI app initialization.
    """
    logger.info("FastAPI application initialization...")
    fastapi_app = FastAPI(
        title="Smart detector service",
        version="0.1.0",
        debug=False,
        description="ML service for for detecting animals in noisy images",
    )
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    fastapi_app.include_router(router, prefix="/api")
    logger.info("FastAPI application has been initialized")
    return fastapi_app


app = get_app()

if __name__ == "__main__":
    logger.info("Starting uvicorn server...")
    uvicorn.run(app, host=HOST, port=PORT)
    logger.info("uvicorn server has been started")
