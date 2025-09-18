#!/usr/bin/env python3
"""
Deployment script for Streamlit Cloud
This script seeds the database and starts the FastAPI backend
"""
import subprocess
import sys
from pathlib import Path

def main():
    # Add backend to Python path
    backend_path = Path(__file__).parent / "backend"
    sys.path.insert(0, str(backend_path))
    
    # Import and run the seed script
    try:
        from backend.seed.seed_db import seed_movies
        print("Seeding database...")
        seed_movies()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        sys.exit(1)
    
    # Start the FastAPI backend
    print("Starting FastAPI backend...")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "backend.app.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

if __name__ == "__main__":
    main()
