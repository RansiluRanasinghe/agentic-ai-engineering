import os
import sys
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Centralized configuration for the agentic monorepo."""

    GROQ_API_KEY: str= os.getenv("GROQ_API_KEY")

    DEFAULT_MODEL: str = "llama3-70b-8192"
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.1

    @classmethod
    def validate(cls):
        """Ensures all critical environment variables are present before booting."""

        if not cls.GROQ_API_KEY:
            print("CRITICAL ERROR: GROQ_API_KEY is missing from the .env file.")
            sys.exit(1)