import os
import sys

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.app import app  # noqa: E402

if __name__ == "__main__":
    print("Starting Flask web server...")
    print("Health endpoint available at: http://127.0.0.1:5000/health")
    app.run(host="0.0.0.0", port=5000, debug=True)
