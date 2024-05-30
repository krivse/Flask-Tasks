from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from app.config import config_app
from app.tasks.models import db
from app.tasks.urls import register_api_tasks


def create_app(mode_test=False):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    # Load .env file in config app.config
    config_app(app, mode_test)
    # Register router tasks to the application
    register_api_tasks(app)
    # Cors configuration
    CORS(app)
    # Swagger configuration
    app.register_blueprint(get_swaggerui_blueprint('/docs', '/static/swagger.json'))
    # Initialize DB
    db.init_app(app)

    with app.app_context():
        # Create database tables for our data models
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
