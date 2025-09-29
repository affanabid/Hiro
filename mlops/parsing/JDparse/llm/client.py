import requests
from .config import OPENROUTER_API_KEY

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_llm(prompt: str, model: str = "deepseek/deepseek-r1-0528-qwen3-8b:free") -> str:
    """
    Send a prompt to OpenRouter API and return the assistant response.
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is not set. Cannot make API request.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(BASE_URL, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
