#!/usr/bin/env python3
"""
Start script for the Meet Room Booking Flask application.
This script sets up the PYTHONPATH and starts the Flask server.
"""
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now we can import from src
from src.app import app

if __name__ == "__main__":
    print("🚀 Starting Meet Room Booking API...")
    print("📍 Health endpoint available at: http://localhost:5000/health")
    print("🔧 API endpoints available at: http://localhost:5000/api/")
    print()

    # Start Flask development server
    app.run(host="0.0.0.0", port=5000, debug=True)
