from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path



# Resolve absolute path to the SQLite DB regardless of current working directory
_BACKEND_DIR = Path(__file__).resolve().parents[1]
_DB_PATH = _BACKEND_DIR / "data" / "movies.db"

# Ensure data directory exists
_DB_PATH.parent.mkdir(exist_ok=True)

class Settings(BaseSettings):
	DATABASE_URL: str = f"sqlite:///{_DB_PATH.as_posix()}"
	API_BASE_PATH: str = ""
	ALLOWED_ORIGINS: List[str] = ["*"]
	DEFAULT_N: int = 10
	MAX_N: int = 20
	SERVICE_VERSION: str = "0.1.0"

	class Config:
		env_file = ".env"


settings = Settings()
