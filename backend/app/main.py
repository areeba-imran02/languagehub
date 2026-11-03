from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401 - register ORM models before metadata use
from app.api.routes import router
from app.core.config import settings
from app.db import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Convenient local development bootstrap. Production deployments should run
    # Alembic migrations as a release step instead of relying on create_all.
    if settings.app_env == "development":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="LanguageHub API",
    version="1.0.0",
    description="Multilingual learning platform API",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "service": "languagehub-api"}
