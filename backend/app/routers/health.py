from fastapi import APIRouter
from ..config import settings
from ..schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
	return HealthResponse(status="ok", version=settings.SERVICE_VERSION)
