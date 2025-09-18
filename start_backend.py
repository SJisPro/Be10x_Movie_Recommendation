#!/usr/bin/env python3
"""
Backend startup script for Streamlit Cloud
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    # Change to backend directory
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    
    # Add backend to Python path
    sys.path.insert(0, str(backend_path))
    
    # Seed the database
    print("Seeding database...")
    subprocess.run([sys.executable, "seed/seed_db.py"], check=True)
    print("Database seeded successfully!")
    
    # Start the FastAPI server
    print("Starting FastAPI server...")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

if __name__ == "__main__":
    main()
