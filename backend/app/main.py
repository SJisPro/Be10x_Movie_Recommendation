from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import init_db
from .routers.health import router as health_router
from .routers.genres import router as genres_router
from .routers.recommendations import router as recommendations_router

app = FastAPI(title="Movie Recommendations API", version=settings.SERVICE_VERSION)

app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.ALLOWED_ORIGINS,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
	init_db()


app.include_router(health_router, prefix=settings.API_BASE_PATH)
app.include_router(genres_router, prefix=settings.API_BASE_PATH)
app.include_router(recommendations_router, prefix=settings.API_BASE_PATH)
