import os
from dotenv import load_dotenv
from google import genai

# تحميل المتغيرات من ملف .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please create a .env file with your API key.")

client = genai.Client(api_key=GEMINI_API_KEY)

# المجالات المدعومة
SUPPORTED_FIELDS = [
    "Web Development",
    "Mobile Development",
    "Data Science",
    "Machine Learning / AI",
    "Cybersecurity",
    "Cloud & DevOps",
    "UI/UX Design",
    "Game Development",
    "Blockchain",
    "Embedded Systems",
]

MASTERY_THRESHOLD = 70

# ربط المجال بلغة البرمجة المناسبة للتقييم العملي
FIELD_TO_LANGUAGE = {
    "Web Development": "javascript",
    "Mobile Development": "kotlin",
    "Data Science": "python",
    "Machine Learning / AI": "python",
    "Cybersecurity": "python",
    "Cloud & DevOps": "python",
    "UI/UX Design": "javascript",
    "Game Development": "csharp",
    "Blockchain": "python",
    "Embedded Systems": "cpp",
}

def get_language_for_field(field: str) -> str:
    """إرجاع لغة البرمجة المناسبة للمجال المطلوب."""
    return FIELD_TO_LANGUAGE.get(field, "python")