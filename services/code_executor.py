import httpx
import asyncio


PISTON_ENDPOINTS = [
    "https://emkc.org/api/v2/piston/execute",  
    "https://piston.kwbar.dev/api/v2/execute",
    "https://piston.deno.dev/api/v2/execute",
]
PISTON_TIMEOUT = 15

SUPPORTED_LANGUAGES = {
    "python": "3.10",
    "javascript": "18.15.0",
    "java": "15.0.2",
    "cpp": "10.2.0",
    "c": "10.2.0",
}

async def run_code(code: str, language: str) -> dict:
    language = language.lower()
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"اللغة غير مدعومة: {language}")
    version = SUPPORTED_LANGUAGES[language]
    payload = {
        "language": language,
        "version": version,
        "files": [{"content": code}],
    }
    last_error = None
    for endpoint in PISTON_ENDPOINTS:
        try:
            async with httpx.AsyncClient(timeout=PISTON_TIMEOUT) as client:
                response = await client.post(endpoint, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    run = result.get("run", {})
                    return {
                        "stdout": run.get("stdout", ""),
                        "stderr": run.get("stderr", ""),
                        "language": language,
                        "version": version,
                    }
                else:
                    last_error = f"HTTP {response.status_code}: {response.text[:100]}"
        except Exception as e:
            last_error = str(e)
    raise RuntimeError(f"فشل تشغيل الكود بعد تجربة جميع endpoints: {last_error}")