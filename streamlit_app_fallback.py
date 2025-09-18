"""
Streamlit app with fallback to mock data if backend fails
"""
import streamlit as st
import requests
import json
from typing import List, Dict, Optional
import time
import os
import subprocess
import threading
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"

# Mock data as fallback
MOCK_MOVIES = [
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genres": ["Drama"],
        "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
    },
    {
        "title": "The Godfather",
        "year": 1972,
        "genres": ["Crime", "Drama"],
        "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
    },
    {
        "title": "The Dark Knight",
        "year": 2008,
        "genres": ["Action", "Crime", "Drama"],
        "overview": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    },
    {
        "title": "Pulp Fiction",
        "year": 1994,
        "genres": ["Crime", "Drama"],
        "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
    },
    {
        "title": "Forrest Gump",
        "year": 1994,
        "genres": ["Drama", "Romance"],
        "overview": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75."
    },
    {
        "title": "Inception",
        "year": 2010,
        "genres": ["Action", "Sci-Fi", "Thriller"],
        "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    },
    {
        "title": "The Matrix",
        "year": 1999,
        "genres": ["Action", "Sci-Fi"],
        "overview": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."
    },
    {
        "title": "Goodfellas",
        "year": 1990,
        "genres": ["Crime", "Drama"],
        "overview": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito."
    }
]

MOCK_GENRES = ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller", "Crime"]

# Page config
st.set_page_config(
    page_title="Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .movie-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .movie-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .movie-year {
        color: #6c757d;
        font-size: 0.9rem;
    }
    .movie-genres {
        margin: 0.5rem 0;
    }
    .genre-tag {
        background-color: #e9ecef;
        color: #495057;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-right: 0.25rem;
        display: inline-block;
    }
    .movie-overview {
        color: #6c757d;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    .demo-notice {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def check_backend_health():
    """Check if backend is running and healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def fetch_genres() -> List[str]:
    """Fetch available genres from the API or return mock data"""
    if check_backend_health():
        try:
            response = requests.get(f"{API_BASE_URL}/genres", timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("genres", [])
        except:
            pass
    
    # Fallback to mock data
    return MOCK_GENRES

def fetch_recommendations(genre: str, n: int, year_min: Optional[int] = None, year_max: Optional[int] = None) -> Dict:
    """Fetch movie recommendations from the API or return mock data"""
    if check_backend_health():
        try:
            params = {"genre": genre, "n": n}
            if year_min is not None:
                params["year_min"] = year_min
            if year_max is not None:
                params["year_max"] = year_max
                
            response = requests.get(f"{API_BASE_URL}/recommendations", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except:
            pass
    
    # Fallback to mock data
    filtered_movies = []
    for movie in MOCK_MOVIES:
        if genre.lower() in [g.lower() for g in movie["genres"]]:
            if year_min and movie["year"] < year_min:
                continue
            if year_max and movie["year"] > year_max:
                continue
            filtered_movies.append(movie)
    
    return {
        "genre": genre,
        "requested": n,
        "returned": len(filtered_movies[:n]),
        "movies": filtered_movies[:n]
    }

def display_movie_card(movie: Dict) -> None:
    """Display a single movie card"""
    genres_html = "".join([f'<span class="genre-tag">{genre}</span>' for genre in movie.get("genres", [])])
    
    st.markdown(f"""
    <div class="movie-card">
        <div class="movie-title">{movie.get("title", "Unknown Title")}</div>
        <div class="movie-year">({movie.get("year", "Unknown Year")})</div>
        <div class="movie-genres">{genres_html}</div>
        <div class="movie-overview">{movie.get("overview", "No description available.")}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.title("🎬 Movie Recommendations")
    st.markdown("Discover your next favorite movie based on genre preferences!")
    
    # Backend status
    if check_backend_health():
        st.success("✅ Backend is running")
    else:
        st.info("📝 Using sample data (backend not available)")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Recommendation Settings")
        
        # Genre selection
        st.subheader("Select Genre")
        genres = fetch_genres()
        
        if not genres:
            st.error("Unable to load genres.")
            st.stop()
        
        selected_genre = st.selectbox(
            "Choose a genre:",
            genres,
            index=0,
            help="Select a genre to get movie recommendations"
        )
        
        # Number of recommendations
        st.subheader("Number of Movies")
        n_movies = st.slider(
            "How many movies would you like?",
            min_value=1,
            max_value=20,
            value=5,
            help="Choose between 1-20 movies"
        )
        
        # Year filters
        st.subheader("Year Filter (Optional)")
        use_year_filter = st.checkbox("Filter by year range")
        
        year_min = None
        year_max = None
        
        if use_year_filter:
            col1, col2 = st.columns(2)
            with col1:
                year_min = st.number_input(
                    "From year:",
                    min_value=1900,
                    max_value=2025,
                    value=1990,
                    step=1
                )
            with col2:
                year_max = st.number_input(
                    "To year:",
                    min_value=1900,
                    max_value=2025,
                    value=2025,
                    step=1
                )
        
        # Get recommendations button
        get_recommendations = st.button(
            "🎯 Get Recommendations",
            type="primary",
            use_container_width=True
        )
    
    # Main content area
    if get_recommendations:
        with st.spinner("Fetching your movie recommendations..."):
            recommendations = fetch_recommendations(
                genre=selected_genre,
                n=n_movies,
                year_min=year_min,
                year_max=year_max
            )
        
        if recommendations:
            genre = recommendations.get("genre", selected_genre)
            requested = recommendations.get("requested", n_movies)
            returned = recommendations.get("returned", 0)
            movies = recommendations.get("movies", [])
            
            # Results header
            st.success(f"Found {returned} movies in the '{genre}' genre!")
            
            if returned < requested:
                st.warning(f"Only {returned} movies available (requested {requested})")
            
            # Display movies
            if movies:
                st.subheader(f"🎬 Your {genre} Movie Recommendations")
                
                for movie in movies:
                    display_movie_card(movie)
            else:
                st.info("No movies found for the selected criteria. Try adjusting your filters.")
        else:
            st.error("Failed to get recommendations. Please try again.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit and FastAPI | "
        "Backend API: [http://localhost:8000](http://localhost:8000) | "
        "API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)"
    )

if __name__ == "__main__":
    main()
