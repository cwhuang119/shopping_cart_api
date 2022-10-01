import os
from datetime import timedelta

class ProductionConfig:
    DEBUG = True
    SECRET_KEY = os.urandom(12).hex(),
    PERMANENT_SESSION_LIFETIME=timedelta(days=31)
    DB_CONNECTION_STR = "sqlite:///project.db"

class TestingConfig:
    DEBUG = True
    SECRET_KEY = os.urandom(12).hex(),
    PERMANENT_SESSION_LIFETIME=timedelta(days=1)
    DB_CONNECTION_STR = "sqlite://"
