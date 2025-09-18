from sqlmodel import SQLModel, create_engine
from .config import settings

# For SQLite, ensure check_same_thread=False so sessions can be used in FastAPI
engine = create_engine(
	settings.DATABASE_URL,
	echo=False,
	connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
)


def init_db() -> None:
	# Import models to ensure they are registered with SQLModel metadata
	from . import models  # noqa: F401
	SQLModel.metadata.create_all(engine)
