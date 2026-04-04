from fastapi import APIRouter, HTTPException
from api.schemas import FinalQuizStartRequest, FinalQuizSubmitRequest, UserContext, QuizRequest
from services.ai_services import generate_quiz
import uuid

router = APIRouter(prefix="/final-quiz", tags=["Final Quiz"])

quiz_sessions = {}

@router.post("/start")
def start_final_quiz(req: FinalQuizStartRequest):
    session_id = str(uuid.uuid4())
    quiz_req = QuizRequest(
        course_title=req.user_context.current_course_title,
        topic=req.user_context.current_phase_title,
        level=req.user_context.level,
        num_questions=10
    )
    quiz_data = generate_quiz(quiz_req)
    quiz_sessions[session_id] = {
        "quiz_data": quiz_data,
        "user_context": req.user_context.dict()
    }
    safe_questions = []
    for q in quiz_data["questions"]:
        safe_q = {k: v for k, v in q.items() if k != "correct_answer"}
        safe_questions.append(safe_q)
    return {
        "session_id": session_id,
        "quiz_title": quiz_data["quiz_title"],
        "questions": safe_questions,
        "practical_task": quiz_data.get("practical_task"),
        "passing_score": quiz_data["passing_score"]
    }

@router.post("/submit")
def submit_final_quiz(req: FinalQuizSubmitRequest):
    session = quiz_sessions.get(req.session_id)
    if not session:
        raise HTTPException(400, "Invalid or expired session")
    quiz_data = session["quiz_data"]
    score = 0
    for i, q in enumerate(quiz_data["questions"]):
        if req.answers.get(str(q["id"])) == q["correct_answer"]:
            score += 1
    score_percent = (score / len(quiz_data["questions"])) * 100
    original_ctx = UserContext(**session["user_context"])
    passed = score_percent >= quiz_data["passing_score"]
    if passed:
        original_ctx.completed_phases.append(original_ctx.current_phase_title)
        original_ctx.current_phase_number += 1
        original_ctx.stage = "learning"
        original_ctx.overall_progress_percent = (original_ctx.current_phase_number / max(original_ctx.total_phases, 1)) * 100
        message = f"تهانينا! اجتزت الاختبار بنسبة {score_percent:.1f}%. انتقل إلى المرحلة التالية."
    else:
        original_ctx.stage = "recovery"
        message = f"نسبة نجاحك {score_percent:.1f}% أقل من {quiz_data['passing_score']}%. راجع نقاط الضعف وحاول مجدداً."
    del quiz_sessions[req.session_id]
    return {
        "passed": passed,
        "score": score_percent,
        "passing_score": quiz_data["passing_score"],
        "updated_user_context": original_ctx,
        "message": message
    }