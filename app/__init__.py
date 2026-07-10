"""
VentureArchitect AI - Flask Application Factory
"""
import logging
import os
from flask import Flask
from flask_cors import CORS


def create_app() -> Flask:
    """Application factory — creates and configures the Flask app."""

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Load config
    from app.config import get_config
    cfg = get_config()

    # Create Flask app
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.config.from_object(cfg)

    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize IBM watsonx.ai service
    try:
        from app.services.watsonx_service import init_watsonx_service
        init_watsonx_service(
            api_key=cfg.IBM_API_KEY,
            project_id=cfg.IBM_PROJECT_ID,
            url=cfg.IBM_WATSONX_URL,
        )
        logger.info("IBM watsonx.ai service initialized successfully.")
    except Exception as exc:
        logger.error("Failed to initialize IBM watsonx.ai service: %s", exc)
        # Don't crash on startup — let requests fail with a clear error message

    # Register blueprints
    from app.routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    logger.info("VentureArchitect AI application created. ENV=%s", os.environ.get("FLASK_ENV", "development"))
    return app
