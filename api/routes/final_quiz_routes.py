import uuid
from fastapi import APIRouter, HTTPException
from api.schemas import FinalQuizStartRequest, FinalQuizSubmitRequest, UserContext, QuizRequest
from services.ai_services import generate_quiz

router = APIRouter(prefix="/final-quiz", tags=["Final Quiz"])


quiz_sessions = {}

@router.post("/start")
def start_final_quiz(req: FinalQuizStartRequest):
    """
    بدء اختبار نهائي للمرحلة الحالية.
    يستخدم البيانات من user_context (current_course_title, current_phase_title, level).
    """
    session_id = str(uuid.uuid4())
    
    
    course_title = req.user_context.current_course_title
    topic = req.user_context.current_phase_title
    level = req.user_context.level
    
    if not course_title or not topic:
        raise HTTPException(
            status_code=400,
            detail="لا يمكن بدء الاختبار النهائي: لم يتم تحديد الكورس الحالي أو الموضوع."
        )
    
   
    quiz_req = QuizRequest(
        course_title=course_title,
        topic=topic,
        level=level,
        num_questions=10
    )
    
    try:
        quiz_data = generate_quiz(quiz_req)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"فشل توليد الاختبار: {str(e)}")
    
    # تخزين جلسة الاختبار
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
    # طباعة debugging (تظهر في terminal السيرفر)
    print(f"Received submit for session_id: {req.session_id}")
    print(f"Available sessions: {list(quiz_sessions.keys())}")
    
    session = quiz_sessions.get(req.session_id)
    if not session:
        raise HTTPException(
            status_code=400,
            detail=f"جلسة الاختبار غير موجودة أو منتهية. المعرف المرسل: {req.session_id}"
        )
    
    quiz_data = session["quiz_data"]
    
    
    if not req.answers:
        raise HTTPException(400, detail="لم يتم إرسال أي إجابات.")
    
   
    score = 0
    total = len(quiz_data["questions"])
    for q in quiz_data["questions"]:
        q_id = str(q["id"])
        user_ans = req.answers.get(q_id)
        if user_ans and user_ans == q["correct_answer"]:
            score += 1
    
    score_percent = (score / total) * 100
    passing_score = quiz_data["passing_score"]
    passed = score_percent >= passing_score
    
    
    original_ctx = UserContext(**session["user_context"])
    
    if passed:
        original_ctx.completed_phases.append(original_ctx.current_phase_title)
        original_ctx.current_phase_number += 1
        original_ctx.stage = "learning"
        if original_ctx.total_phases > 0:
            original_ctx.overall_progress_percent = (original_ctx.current_phase_number / original_ctx.total_phases) * 100
        message = f"تهانينا! اجتزت الاختبار بنسبة {score_percent:.1f}%. انتقل إلى المرحلة التالية."
    else:
        original_ctx.stage = "recovery"
        message = f"نسبة نجاحك {score_percent:.1f}% أقل من {passing_score}%. راجع نقاط الضعف وحاول مجدداً."
    
    
    del quiz_sessions[req.session_id]
    
    return {
        "passed": passed,
        "score": score_percent,
        "passing_score": passing_score,
        "updated_user_context": original_ctx,
        "message": message
    }