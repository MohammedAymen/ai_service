import json
import time
from google.genai import types
from core.config import client

MODELS = [
    "gemini-3-flash-preview",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash"
]

def call_gemini(prompt: str, required_keys: set[str], max_retries: int = 3) -> dict:
    last_error = None

    for attempt in range(max_retries):
        for model in MODELS:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.65,
                        top_p=0.9,
                        response_mime_type="application/json",
                    ),
                )
                data = json.loads(response.text)
                missing = required_keys - data.keys()
                if missing:
                    continue
                return data
            except Exception as e:
                last_error = e
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    time.sleep(2 ** attempt)
                continue

    raise last_error or Exception("Gemini غير متاح حالياً")


def call_gemini_chat(prompt: str) -> dict:
    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.9,
                    top_p=0.9,
                    response_mime_type="application/json",
                ),
            )
            return json.loads(response.text)
        except Exception:
            continue

    raise Exception("Gemini غير متاح حالياً")