from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from ..config import settings
from ..db import engine
from ..schemas import RecommendationsResponse, MovieOut
from ..services import RecommendationService
from ..repositories import GenreRepository

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_session():
	with Session(engine) as session:
		yield session


@router.get("", response_model=RecommendationsResponse)
def recommend(
	genre: str = Query(..., description="Genre name"),
	n: int = Query(settings.DEFAULT_N, ge=1, le=settings.MAX_N),
	year_min: int | None = Query(default=None),
	year_max: int | None = Query(default=None),
	session: Session = Depends(get_session),
) -> RecommendationsResponse:
	genre_obj = GenreRepository.get_by_name(session, genre)
	if genre_obj is None:
		raise HTTPException(status_code=400, detail=f"Unknown genre: {genre}")

	movies_dict = RecommendationService.recommend_by_genre(session, genre, n, year_min, year_max)
	movies_out = [MovieOut(**m) for m in movies_dict]
	return RecommendationsResponse(
		genre=genre,
		requested=n,
		returned=len(movies_out),
		movies=movies_out,
	)
