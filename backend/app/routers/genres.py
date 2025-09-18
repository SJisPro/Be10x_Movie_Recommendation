from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..db import engine
from ..schemas import GenreListResponse
from ..services import RecommendationService

router = APIRouter(prefix="/genres", tags=["genres"])


def get_session():
	with Session(engine) as session:
		yield session


@router.get("", response_model=GenreListResponse)
def list_genres(session: Session = Depends(get_session)) -> GenreListResponse:
	genres = RecommendationService.get_genres(session)
	return GenreListResponse(genres=genres)
