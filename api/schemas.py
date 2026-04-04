from typing import Literal
from pydantic import BaseModel, Field


# ══════════════════════════════════════════════
# مسار التعلم
# ══════════════════════════════════════════════

class LearningPathRequest(BaseModel):
    goal: str            = Field(..., example="عاوز أبقى مطور خلفي")
    field: str           = Field(..., example="Web Development")
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    background: str      = Field(..., example="درست أساسيات وعارف شوية بايثون")
    hours_per_day: float = Field(..., ge=0.5, le=8.0, example=2.0)
    language: Literal["Arabic", "English", "Both"] = "Both"
    target_months: int   = Field(..., ge=1, le=24, example=6)


# ══════════════════════════════════════════════
# الاختبار
# ══════════════════════════════════════════════

class QuizRequest(BaseModel):
    course_title: str  = Field(..., example="Python for Everybody")
    topic: str         = Field(..., example="Functions and Recursion")
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    num_questions: int = Field(default=5, ge=3, le=10)


# ══════════════════════════════════════════════
# التقرير الأسبوعي
# ══════════════════════════════════════════════

class WeeklyReportRequest(BaseModel):
    week_number: int         = Field(..., ge=1, example=3)
    path_title: str          = Field(..., example="مطور خلفي محترف")
    completed_topics: list[str]
    quiz_scores: list[float] = Field(..., description="درجات من 0 لـ 100")
    hours_studied: float     = Field(..., description="ساعات الدراسة الفعلية")
    target_hours: float      = Field(..., description="ساعات الدراسة المستهدفة")
    struggles: str           = Field(default="", example="بفهم الـ async بصعوبة")


# ══════════════════════════════════════════════
# إعادة التوجيه
# ══════════════════════════════════════════════

class RerouteRequest(BaseModel):
    path_title: str        = Field(..., example="تعلم الآلة والذكاء الاصطناعي")
    current_phase: str     = Field(..., example="المرحلة الثانية — خوارزميات التعلم")
    mastery_score: float   = Field(..., ge=0, le=100, example=45.0)
    weak_topics: list[str] = Field(..., example=["الانحدار الخطي", "النزول التدريجي"])
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"


# ══════════════════════════════════════════════
# الشات — بيانات المستخدم الكاملة
# ══════════════════════════════════════════════

class ChatMessage(BaseModel):
    """رسالة واحدة في تاريخ المحادثة."""
    role: Literal["user", "assistant"]
    content: str


class UserContext(BaseModel):
    """
    بيانات المستخدم الكاملة.
    الخادم بيجيبها من قاعدة البيانات ويبعتها مع كل رسالة.
    """
    # بيانات شخصية
    name: str
    goal: str                        = Field(default="")
    field: str                       = Field(default="")
    level: str                       = Field(default="")
    started_at: str                  = Field(default="")

    # المرحلة الحالية في الأبليكيشن
    stage: Literal[
        "assessment",   # تيست مستوى — أول ما يدخل
        "onboarding",   # شرح الرود ماب وتحديد المستوى
        "learning",     # متابعة ومذاكرة
    ] = "assessment"

    # بيانات المسار — بتتملى بعد الـ assessment
    path_title: str                  = Field(default="")
    total_phases: int                = Field(default=0)
    current_phase_number: int        = Field(default=0)
    current_phase_title: str         = Field(default="")
    current_course_title: str        = Field(default="")
    current_course_url: str          = Field(default="")
    completed_phases: list[str]      = Field(default=[])

    # بيانات التقدم
    completed_topics: list[str]      = Field(default=[])
    remaining_topics: list[str]      = Field(default=[])
    overall_progress_percent: float  = Field(default=0.0)

    # بيانات الأداء
    quiz_scores: list[float]         = Field(default=[])
    average_quiz_score: float        = Field(default=0.0)
    strong_topics: list[str]         = Field(default=[])
    weak_topics: list[str]           = Field(default=[])

    # بيانات الوقت
    hours_per_day: float             = Field(default=0.0)
    hours_studied_this_week: float   = Field(default=0.0)
    target_hours_this_week: float    = Field(default=0.0)
    total_hours_studied: float       = Field(default=0.0)

    # ملاحظات
    struggles: str                   = Field(default="")
    last_activity: str               = Field(default="")


class ChatRequest(BaseModel):
    message: str
    user_context: UserContext
    chat_history: list[ChatMessage]  = Field(
        default=[],
        description="تاريخ المحادثة — بيبعته الخادم عشان جيميني يفضل فاكر السياق"
    )


# ══════════════════════════════════════════════
# مراجعة الكود
# ══════════════════════════════════════════════

class CodeReviewRequest(BaseModel):
    code: str            = Field(..., example="def add(a, b):\n    return a + b")
    language: str        = Field(default="python", example="python")
    question: str        = Field(..., example="اكتب دالة تجمع رقمين")
    user_level: Literal["beginner", "intermediate", "advanced"] = "beginner"


# ─────────────────────────────────────────────────────────────
# Assessment
# ─────────────────────────────────────────────────────────────
class AssessmentStartRequest(BaseModel):
    user_context: UserContext
    field: str
    goal: str = ""

class AssessmentAnswerRequest(BaseModel):
    session_id: str
    answer: str

# ─────────────────────────────────────────────────────────────
# Final Quiz
# ─────────────────────────────────────────────────────────────
class FinalQuizStartRequest(BaseModel):
    user_context: UserContext

class FinalQuizSubmitRequest(BaseModel):
    session_id: str
    answers: dict
    user_context: UserContext