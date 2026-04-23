import requests
from app.config import Config


def generate_from_llm(prompt: str):
    if Config.OPENROUTER_API_KEY:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": Config.OPENROUTER_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that returns strict JSON output when asked.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
            },
            timeout=30,
        )

        if response.status_code != 200:
            raise Exception(f"LLM request failed: {response.text}")

        data = response.json()
        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )
        return {"response": content}

    if not Config.BASE_URL or not Config.LLM_TOKEN:
        raise Exception("LLM is not configured. Set OPENROUTER_API_KEY or LLM_BASE_URL + LLM_TOKEN")

    response = requests.post(
        f"{Config.BASE_URL}/llm/chat",
        json={
            "token": Config.LLM_TOKEN,
            "chat": prompt,
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise Exception(f"LLM request failed: {response.text}")

    return response.json()