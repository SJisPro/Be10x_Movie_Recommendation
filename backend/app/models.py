from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class MovieGenre(SQLModel, table=True):
	movie_id: Optional[int] = Field(default=None, foreign_key="movie.id", primary_key=True, index=True)
	genre_id: Optional[int] = Field(default=None, foreign_key="genre.id", primary_key=True, index=True)


class Movie(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	title: str = Field(index=True)
	year: Optional[int] = Field(default=None, index=True)
	overview: Optional[str] = None
	poster_url: Optional[str] = None

	genres: List["Genre"] = Relationship(back_populates="movies", link_model=MovieGenre)


class Genre(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str = Field(index=True, unique=True)

	movies: List[Movie] = Relationship(back_populates="genres", link_model=MovieGenre)
