import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Settings for configuration from .env file."""
    def __init__(self, mode_test):
        self.MODE_TEST = mode_test
        # General Config
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.FLASK_APP = os.getenv('FLASK_APP')
        # Settings for dev and testing environment
        if self.MODE_TEST is False:
            self.SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
        else:
            self.SQLALCHEMY_DATABASE_URI = os.getenv('TEST_SQLALCHEMY_DATABASE_URI')
        self.SQLALCHEMY_ECHO = False
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False


def config_app(app, mode_test):
    """Load config from .env file."""
    app.config.from_object(Config(mode_test))

