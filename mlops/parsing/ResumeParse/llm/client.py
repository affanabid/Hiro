import requests
import os
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === Configuration ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# === Function to call Groq API ===
def call_groq(prompt: str, model: str = "llama-3.1-8b-instant", temperature: float = 0.0):
    """
    Call GROQ API with robust error handling and JSON extraction.

    Args:
        prompt: The text prompt to send.
        model: Model to use (default: llama-3.1-8b-instant).
        temperature: Temperature setting (0.0 for deterministic output).

    Returns:
        Cleaned response text (JSON or plain text).
    """
    if not GROQ_API_KEY:
        raise ValueError("❌ GROQ_API_KEY not found in environment variables. Please check your .env file.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a precise resume parser that outputs strict JSON only. "
                    "Never include markdown, comments, or explanations — only valid JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": temperature
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)

        # Debug: Print the raw response if something fails
        if response.status_code != 200:
            print("🔍 Status Code:", response.status_code)
            print("🔍 Response Text:", response.text)

        response.raise_for_status()
        data = response.json()

        content = data["choices"][0]["message"]["content"]
        cleaned_content = extract_json_from_response(content)

        return cleaned_content

    except requests.exceptions.Timeout:
        raise Exception("⏰ GROQ API request timed out.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"🚨 GROQ API request failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise Exception(f"⚠️ Invalid response format from GROQ: {str(e)}")


# === Helper: Clean JSON from response ===
def extract_json_from_response(text: str) -> str:
    """
    Extract JSON from LLM response that might include markdown or extra text.
    """
    # Remove markdown code blocks
    if "```json" in text:
        match = re.search(r'```json\s*\n?(.*?)\n?```', text, re.DOTALL)
        if match:
            return match.group(1).strip()

    if "```" in text:
        match = re.search(r'```\s*\n?(.*?)\n?```', text, re.DOTALL)
        if match:
            return match.group(1).strip()

    # Try to find JSON object in plain text
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        json_str = text[start:end+1]
        try:
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            pass

    return text.strip()


# === Test Groq Connection ===
def test_groq_connection():
    """
    Test if GROQ API connection works.
    """
    test_prompt = 'Return only this JSON: {"status": "ok"}'
    try:
        response = call_groq(test_prompt)
        print("✅ GROQ API connection successful")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print(f"❌ GROQ API connection failed: {e}")
        return False


# === Main Execution ===
if __name__ == "__main__":
    test_groq_connection()
