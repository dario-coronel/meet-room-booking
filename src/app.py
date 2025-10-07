from src.controllers.health_controller import create_app

# Create Flask application
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
