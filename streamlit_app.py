"""
Streamlit Cloud entry point
This file serves as the main entry point for Streamlit Cloud deployment
"""
import os
import subprocess
import threading
import time
from pathlib import Path

# Start the FastAPI backend in a separate thread
def start_backend():
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    
    # Seed the database first
    try:
        subprocess.run([os.sys.executable, "seed/seed_db.py"], check=True)
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
    
    # Start the FastAPI server
    subprocess.run([
        os.sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

# Start backend in background
backend_thread = threading.Thread(target=start_backend, daemon=True)
backend_thread.start()

# Wait a moment for backend to start
time.sleep(3)

# Import and run the Streamlit app
from frontend.app import *
