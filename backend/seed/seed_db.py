import json
import sys
from pathlib import Path
from typing import Dict, List

# Add the parent directory to the path so we can import from backend
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlmodel import Session, select

from backend.app.db import engine
from backend.app.models import Movie, Genre, MovieGenre

SEED_FILE = Path(__file__).with_name("seed_movies.json")


def get_or_create_genre(session: Session, name: str) -> Genre:
	genre = session.exec(select(Genre).where(Genre.name == name)).first()
	if genre:
		return genre
	genre = Genre(name=name)
	session.add(genre)
	session.commit()
	session.refresh(genre)
	return genre


def seed_movies() -> None:
	with open(SEED_FILE, "r", encoding="utf-8") as f:
		payload: List[Dict] = json.load(f)

	with Session(engine) as session:
		for entry in payload:
			title = entry["title"]
			year = entry.get("year")
			overview = entry.get("overview")
			poster_url = entry.get("poster_url")
			genre_names = entry.get("genres", [])

			movie = Movie(title=title, year=year, overview=overview, poster_url=poster_url)
			session.add(movie)
			session.commit()
			session.refresh(movie)

			for gname in genre_names:
				genre = get_or_create_genre(session, gname)
				link = MovieGenre(movie_id=movie.id, genre_id=genre.id)
				session.add(link)
			session.commit()

	print(f"Seeded {len(payload)} movies from {SEED_FILE}")


if __name__ == "__main__":
	seed_movies()
