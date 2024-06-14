import os
from pathlib import Path

from dotenv import load_dotenv

# Local .env file
PATH_ENV = Path(__file__).parent.parent / ".env"

load_dotenv(PATH_ENV)

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

SELENIUM_HOST = os.environ.get("SELENIUM_HOST")
