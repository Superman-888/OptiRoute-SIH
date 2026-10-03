import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME = "Quantum-Inspired Intelligent Traffic Route Optimization"
    APP_VERSION = "1.0.0"

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    LIGHTGBM_MODEL_PATH = os.getenv(
        "LIGHTGBM_MODEL_PATH",
        "models/lightgbm_model.txt"
    )


settings = Settings()