import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

print(f"Testing OpenRouter API Key...")
print(f"API Key present: {bool(api_key)}")
if api_key:
    print(f"Key prefix: {api_key[:20]}...")
    print(f"Key length: {len(api_key)}")

print(f"Model: {model}")
print()

if not api_key:
    print("ERROR: OPENROUTER_API_KEY not set in .env")
    exit(1)

try:
    print("Sending test request to OpenRouter...")
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "Say 'OK' in one word",
                }
            ],
            "temperature": 0.7,
            "max_tokens": 10,
        },
        timeout=10,
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✓ SUCCESS: API key is valid and OpenRouter is working!")
    else:
        print(f"\n✗ FAILED: {response.status_code}")
        print(f"Error details: {response.json()}")

except Exception as e:
    print(f"✗ ERROR: {str(e)}")
