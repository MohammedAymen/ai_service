"""
خدمة تشغيل الكود عن طريق Piston API.
مجاني 100% — من غير تسجيل أو مفتاح.
"""

import httpx

PISTON_URL     = "https://emkc.org/api/v2/piston/execute"
PISTON_TIMEOUT = 10  # ثواني

SUPPORTED_LANGUAGES = {
    "python"     : "3.10",
    "javascript" : "18.15.0",
    "java"       : "15.0.2",
    "cpp"        : "10.2.0",
    "c"          : "10.2.0",
}


async def run_code(code: str, language: str) -> dict:
    """
    يبعت الكود لـ Piston يشغله ويرجع النتيجة.

    Returns:
        {
            "stdout": str,
            "stderr": str,
            "language": str,
            "version": str,
        }

    Raises:
        ValueError: لو اللغة مش مدعومة.
        RuntimeError: لو Piston مرجعش رد.
    """
    language = language.lower()

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"اللغة '{language}' مش مدعومة. "
            f"اللغات المتاحة: {list(SUPPORTED_LANGUAGES.keys())}"
        )

    version = SUPPORTED_LANGUAGES[language]

    async with httpx.AsyncClient(timeout=PISTON_TIMEOUT) as client:
        response = await client.post(
            PISTON_URL,
            json={
                "language" : language,
                "version"  : version,
                "files"    : [{"content": code}],
            },
        )
        response.raise_for_status()

    result = response.json()
    run    = result.get("run", {})

    return {
        "stdout"   : run.get("stdout", ""),
        "stderr"   : run.get("stderr", ""),
        "language" : language,
        "version"  : version,
    }
