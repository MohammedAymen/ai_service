from api.schemas import CodeReviewRequest


def build_code_review_prompt(r: CodeReviewRequest, execution_result: dict) -> str:
    stdout   = execution_result.get("stdout", "").strip()
    stderr   = execution_result.get("stderr", "").strip()
    is_error = bool(stderr)

    return f"""
أنت مدرس برمجة محترف بتراجع كود طالب وبتديه تغذية راجعة مخصصة.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
تفاصيل التمرين
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
السؤال    : {r.question}
اللغة     : {r.language}
المستوى   : {r.user_level}

الكود اللي كتبه الطالب:
{r.code}

نتيجة تشغيل الكود:
# بعد ✅
{("❌ في خطأ:" + chr(10) + stderr) if is_error else ("✅ الكود اشتغل:" + chr(10) + (stdout or "مفيش output"))}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

قواعد الرد:
1. ارجع JSON بس — من غير أي كلام تاني
2. الرد يكون على حسب اللغه بتاعت المستخدم — لو بيكتب بالعربي، رد بالعربي، ولو بالإنجليزي، رد بالإنجليزي
3. التغذية الراجعة تكون مناسبة لمستوى الطالب: {r.user_level}
4. لو في خطأ — اشرح إيه المشكلة وإزاي يصلحها بوضوح
5. لو الكود صح — قوله إيه اللي عمله كويس وإزاي يحسنه

ارجع الـ JSON ده بالظبط:
{{
  "is_correct": boolean,
  "score": number,
  "execution_status": "success" | "error",
  "feedback": {{
    "summary": string,
    "what_went_wrong": string | null,
    "how_to_fix": string | null,
    "what_is_good": string | null,
    "how_to_improve": string | null
  }},
  "corrected_code": string | null,
  "key_concepts_to_review": [string]
}}
""".strip()
