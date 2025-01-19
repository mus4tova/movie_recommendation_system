import os.path
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"
if not os.path.isdir(MODEL_DIR):
    os.mkdir(MODEL_DIR)

class Settings(BaseSettings):
    TMDB_API_KEY: str
    model_config = SettingsConfigDict(env_file=BASE_DIR/".env")


# MLflow
TRACKING_URI = "http://13.60.52.168:5000"

# MLflow
TMDB_API_KEY = Settings().TMDB_API_KEY