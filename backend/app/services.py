import random
from typing import List, Optional
from sqlmodel import Session

from .config import settings
from .models import Movie
from .repositories import GenreRepository, MovieRepository


def movie_to_dict(session: Session, movie: Movie) -> dict:
	# Fetch genres via relationship (already lazy-loaded by SQLModel when accessed)
	genre_names = [g.name for g in movie.genres]
	return {
		"id": movie.id,
		"title": movie.title,
		"year": movie.year,
		"genres": genre_names,
		"overview": movie.overview,
		"poster_url": movie.poster_url,
	}


class RecommendationService:
	@staticmethod
	def get_genres(session: Session) -> List[str]:
		return GenreRepository.list_genre_names(session)

	@staticmethod
	def recommend_by_genre(
		session: Session,
		genre_name: str,
		n: Optional[int] = None,
		year_min: Optional[int] = None,
		year_max: Optional[int] = None,
	) -> List[dict]:
		requested_n = n if n is not None else settings.DEFAULT_N
		requested_n = max(1, min(settings.MAX_N, requested_n))

		pool = MovieRepository.list_by_genre(session, genre_name, year_min, year_max)
		if not pool:
			return []

		k = min(requested_n, len(pool))
		sampled = random.sample(pool, k)
		return [movie_to_dict(session, m) for m in sampled]
