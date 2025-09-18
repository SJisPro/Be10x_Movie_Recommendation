# Movie Recommendations Backend (FastAPI + SQLite)

## Setup
1. Create a virtual environment and install dependencies:
```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run API (dev):
```
uvicorn backend.app.main:app --reload --port 8000
```

3. Initialize DB and seed:
```
python -c "from backend.app.db import init_db; init_db()"
python backend/seed/seed_db.py
```

## Endpoints
- GET `/health`
- GET `/genres`
- GET `/recommendations?genre=Action&n=10` (optional `year_min`, `year_max`)

## Config
Edit `.env` (optional):
```
DATABASE_URL=sqlite:///./backend/data/movies.db
API_BASE_PATH=
ALLOWED_ORIGINS=["*"]
DEFAULT_N=10
MAX_N=20
SERVICE_VERSION=0.1.0
```
