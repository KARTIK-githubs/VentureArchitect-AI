"""
VentureArchitect AI - Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""

    # Flask
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    TESTING = False

    # App
    APP_NAME = os.environ.get("APP_NAME", "VentureArchitect AI")
    APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")

    # IBM watsonx.ai
    IBM_API_KEY = os.environ.get("IBM_API_KEY")
    IBM_PROJECT_ID = os.environ.get("IBM_PROJECT_ID")
    IBM_WATSONX_URL = os.environ.get("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

    # LLM defaults
    DEFAULT_MODEL_ID = "meta-llama/llama-3-3-70b-instruct"
    DEFAULT_MAX_NEW_TOKENS = 1500
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_TOP_P = 0.9
    DEFAULT_TOP_K = 50
    DEFAULT_REPETITION_PENALTY = 1.1


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config():
    env = os.environ.get("FLASK_ENV", "development")
    return config_map.get(env, config_map["default"])
