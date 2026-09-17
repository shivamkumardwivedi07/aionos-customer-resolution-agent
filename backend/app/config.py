import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")

DATA_DIR = Path(__file__).resolve().parent / "data"

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
AGENT_MODE = os.getenv("AGENT_MODE", "hybrid")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

EXERCISE_DATE = "Wednesday, 23 September 2026"
AGENT_WAIVER_LIMIT_INR = 1500.0
