#!/usr/bin/env python3
"""
Simple script to run the Streamlit frontend
"""
import subprocess
import sys
import os

def main():
    # Change to frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    os.chdir(frontend_dir)
    
    # Run streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"], check=True)
    except KeyboardInterrupt:
        print("\nShutting down frontend...")
    except subprocess.CalledProcessError as e:
        print(f"Error running frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
