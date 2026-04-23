import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_PORT = os.getenv("APP_PORT")
    BASE_URL = os.getenv("LLM_BASE_URL")
    LLM_TOKEN = os.getenv("LLM_TOKEN")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False