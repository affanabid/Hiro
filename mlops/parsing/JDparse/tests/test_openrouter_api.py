import os
import sys
import requests
import json

# Use an environment variable for the API key to avoid committing secrets.
api_key = "api_key"
# if not api_key:
#     print("Error: OPENROUTER_API_KEY environment variable is not set.\n" \
#           "Set it and re-run the script. Example (cmd.exe):\n" \
#           "  set OPENROUTER_API_KEY=sk-...\n")
#     sys.exit(1)

payload = {
    "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
    "messages": [
        {"role": "user", "content": "What is the meaning of life?"}
    ]
}

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional
        # "X-Title": "<YOUR_SITE_NAME>", # Optional
    },
    data=json.dumps(payload)
)

print("Status:", response.status_code)
try:
    # pretty-print JSON response when possible
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except ValueError:
    print("Response text:")
    print(response.text)