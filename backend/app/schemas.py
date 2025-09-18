from typing import List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
	status: str
	version: str


class GenreListResponse(BaseModel):
	genres: List[str]


class MovieOut(BaseModel):
	id: int
	title: str
	year: Optional[int] = None
	genres: List[str] = Field(default_factory=list)
	overview: Optional[str] = None
	poster_url: Optional[str] = None


class RecommendationsResponse(BaseModel):
	genre: str
	requested: int
	returned: int
	movies: List[MovieOut]
