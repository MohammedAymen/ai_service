import json
from google.genai import types
from core.config import client


def call_gemini(prompt: str, required_keys: set[str]) -> dict:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.75,
            top_p=0.9,
            response_mime_type="application/json",
        ),
    )

    data = json.loads(response.text)

    missing = required_keys - data.keys()
    if missing:
        raise ValueError(f"الرد ناقص keys: {missing}")

    return data


def call_gemini_chat(prompt: str) -> dict:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.75,
            top_p=0.9,
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)