from fastapi import APIRouter, HTTPException

from api.schemas import (
    LearningPathRequest,
    QuizRequest,
    WeeklyReportRequest,
    RerouteRequest,
    ChatRequest,
    CodeReviewRequest,
)
from core.config import SUPPORTED_FIELDS, MASTERY_THRESHOLD
from services.ai_services import (
    generate_learning_path,
    generate_quiz,
    generate_weekly_report,
    generate_reroute,
    generate_chat_reply,
    review_code,
)

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/learning-path", summary="توليد مسار تعليمي مخصص")
def learning_path(request: LearningPathRequest):
    if request.field not in SUPPORTED_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"المجال مش مدعوم. المجالات المتاحة: {SUPPORTED_FIELDS}",
        )
    try:
        return {"status": "success", "data": generate_learning_path(request)}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quiz", summary="توليد اختبار بعد إنهاء وحدة")
def quiz(request: QuizRequest):
    try:
        return {"status": "success", "data": generate_quiz(request)}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/weekly-report", summary="توليد تقرير أداء أسبوعي")
def weekly_report(request: WeeklyReportRequest):
    try:
        return {"status": "success", "data": generate_weekly_report(request)}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reroute", summary="خطة إنقاذ لو الدرجة أقل من 70%")
def reroute(request: RerouteRequest):
    if request.mastery_score >= MASTERY_THRESHOLD:
        raise HTTPException(
            status_code=400,
            detail=f"الدرجة {request.mastery_score}% — إعادة التوجيه بتشتغل بس لو أقل من {MASTERY_THRESHOLD}%",
        )
    try:
        return {"status": "success", "data": generate_reroute(request)}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", summary="شات مع المساعد الشخصي")
def chat(request: ChatRequest):
    try:
        result = generate_chat_reply(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/code-review", summary="تشغيل الكود ومراجعته")
async def code_review(request: CodeReviewRequest):
    try:
        result = await review_code(request)
        return {"status": "success", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
