import requests
from app.config import Config


def _build_auth_header(token: str) -> dict:
    clean = (token or "").strip()
    if not clean:
        return {}

    # Avoid double prefix if token already includes a scheme.
    if clean.lower().startswith("bearer "):
        value = clean
    else:
        value = f"Bearer {clean}"

    return {"Authorization": value}


def generate_from_llm(prompt: str):
    custom_token = (Config.LLM_TOKEN or "").strip()
    if not custom_token and Config.BASE_URL:
        # Backward-compatible fallback for projects that still store one token only.
        custom_token = (Config.OPENROUTER_API_KEY or "").strip()

    if Config.BASE_URL and custom_token:
        response = requests.post(
            f"{Config.BASE_URL}/llm/chat",
            headers={
                **_build_auth_header(custom_token),
                "Content-Type": "application/json",
            },
            json={
                # Keep token in payload for backward compatibility with older gateways.
                "token": custom_token,
                "chat": prompt,
            },
            timeout=30,
        )

        if response.status_code != 200:
            raise Exception(f"LLM request failed: {response.text}")

        return response.json()

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

    raise Exception("LLM is not configured. Set LLM_BASE_URL + LLM_TOKEN (recommended) or OPENROUTER_API_KEY")