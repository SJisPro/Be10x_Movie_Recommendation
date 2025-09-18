from typing import List, Optional
from sqlmodel import Session, select

from .models import Movie, Genre, MovieGenre


class GenreRepository:
	@staticmethod
	def list_genre_names(session: Session) -> List[str]:
		statement = select(Genre.name).order_by(Genre.name)
		return list(session.exec(statement).all())

	@staticmethod
	def get_by_name(session: Session, name: str) -> Optional[Genre]:
		statement = select(Genre).where(Genre.name == name)
		return session.exec(statement).first()


class MovieRepository:
	@staticmethod
	def list_by_genre(
		session: Session,
		genre_name: str,
		year_min: Optional[int] = None,
		year_max: Optional[int] = None,
	) -> List[Movie]:
		# Join movies -> movie_genres -> genres filtering by name
		statement = (
			select(Movie)
			.join(MovieGenre, Movie.id == MovieGenre.movie_id)
			.join(Genre, Genre.id == MovieGenre.genre_id)
			.where(Genre.name == genre_name)
		)

		if year_min is not None:
			statement = statement.where(Movie.year >= year_min)
		if year_max is not None:
			statement = statement.where(Movie.year <= year_max)

		return list(session.exec(statement).all())
