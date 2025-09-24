from src.controllers.health_controller import create_app
from src.controllers.booking_controller import api_bp

# Create Flask app with health endpoint
app = create_app()

# Register API blueprint for booking management
app.register_blueprint(api_bp)

if __name__ == '__main__':
    # Run Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True)