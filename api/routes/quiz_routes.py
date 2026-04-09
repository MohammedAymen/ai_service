from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from core.gemini_client import call_gemini
from api.schemas import UserContext

router = APIRouter(prefix="/quiz", tags=["Quiz"])

class QuizSubmitRequest(BaseModel):
    answers: Dict[str, str]
    questions: List[Dict[str, Any]]
    passing_score: int
    language: str = "English"
    user_context: Optional[UserContext] = None  # اختياري

class QuestionResult(BaseModel):
    id: int
    question: str
    user_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str
    topic: str

class QuizSubmitResponse(BaseModel):
    score: int
    total: int
    percentage: float
    passed: bool
    passing_score: int
    results: List[QuestionResult]
    summary: str
    recommendation: str

@router.post("/submit", response_model=QuizSubmitResponse)
async def submit_quiz(req: QuizSubmitRequest):
    total = len(req.questions)
    score = 0
    results = []

    for q in req.questions:
        qid = str(q["id"])
        user_ans = req.answers.get(qid, "").upper().strip()
        correct_ans = q.get("correct_answer", "").upper().strip()
        is_correct = (user_ans == correct_ans)
        if is_correct:
            score += 1
        results.append(QuestionResult(
            id=q["id"],
            question=q["question"],
            user_answer=user_ans if user_ans else "(لم يجب)",
            correct_answer=correct_ans,
            is_correct=is_correct,
            explanation=q.get("explanation", "لا يوجد شرح"),
            topic=q.get("topic", "عام")
        ))

    percentage = (score / total) * 100
    passed = percentage >= req.passing_score

    # إنشاء ملخص وتوصية باستخدام Gemini
    try:
        lang = req.language
        prompt = f"""
You are an expert teacher. Based on the following quiz results, write a short summary (two sentences) and one recommendation for improvement. Respond in {lang} language ONLY.

Results:
{chr(10).join([f"- Question {r.id}: {'correct' if r.is_correct else 'wrong'} - Topic: {r.topic}" for r in results])}
Score: {score}/{total} ({percentage:.1f}%)
Passing score: {req.passing_score}%

Return JSON: {{"summary": "...", "recommendation": "..."}}
"""
        feedback = call_gemini(prompt, {"summary", "recommendation"})
        summary = feedback["summary"]
        recommendation = feedback["recommendation"]
    except Exception:
        # Fallback
        if passed:
            summary = f"أحسنت! أجبت على {score} من {total} ({percentage:.1f}%). اجتزت الاختبار!"
            recommendation = "واصل تقدمك إلى الموضوع التالي."
        else:
            wrong_topics = list(set(r.topic for r in results if not r.is_correct))
            summary = f"حصلت على {score} من {total} ({percentage:.1f}%). لم تجتز الاختبار."
            recommendation = f"راجع هذه المواضيع: {', '.join(wrong_topics[:3])} ثم حاول مرة أخرى."

    return QuizSubmitResponse(
        score=score, total=total, percentage=percentage,
        passed=passed, passing_score=req.passing_score,
        results=results, summary=summary, recommendation=recommendation
    )