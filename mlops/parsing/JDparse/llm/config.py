import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the first parent directory that contains it
def load_env():
    for p in Path(__file__).resolve().parents:
        env_path = p / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=str(env_path))
            return str(env_path)
    return None

_loaded_env = load_env()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if OPENROUTER_API_KEY:
    print(f"Using key: {OPENROUTER_API_KEY}")
else:
    print("Warning: OPENROUTER_API_KEY is not set. Please set it to use the LLM client.")
