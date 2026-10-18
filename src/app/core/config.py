from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    PROJECT_NAME: str = "AI Code Debugger API"
    VERSION: str = "1.0.0"
    API_KEY: str = os.getenv("GEMINI_API_KEY")
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: list = [os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")]


settings = Settings()

if not settings.API_KEY:
    raise ValueError("Debugger_API_KEY environment variable is missing!")
