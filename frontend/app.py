import streamlit as st
import requests
import json
from typing import List, Dict, Optional
import time

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

def fetch_genres() -> List[str]:
    """Fetch available genres from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/genres", timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("genres", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch genres: {str(e)}")
        return []

def fetch_recommendations(genre: str, n: int, year_min: Optional[int] = None, year_max: Optional[int] = None) -> Dict:
    """Fetch movie recommendations from the API"""
    try:
        params = {"genre": genre, "n": n}
        if year_min is not None:
            params["year_min"] = year_min
        if year_max is not None:
            params["year_max"] = year_max
            
        response = requests.get(f"{API_BASE_URL}/recommendations", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch recommendations: {str(e)}")
        return {}

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
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Recommendation Settings")
        
        # Genre selection
        st.subheader("Select Genre")
        genres = fetch_genres()
        
        if not genres:
            st.error("Unable to load genres. Please check if the backend is running.")
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
            value=10,
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
                    value=2010,
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
