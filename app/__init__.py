from app.db import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register startup event to initialize the database
    @app.on_event("startup")
    async def startup():
        await init_db()  # Initialize the database asynchronously

    return app