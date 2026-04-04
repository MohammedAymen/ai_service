from fastapi import APIRouter, HTTPException
from api.schemas import AssessmentStartRequest, AssessmentAnswerRequest, UserContext, CodeReviewRequest
from core.gemini_client import call_gemini
from core.config import get_language_for_field
from prompts.assessment_prompt import (
    build_assessment_question_prompt,
    build_coding_question_prompt,
    build_assessment_final_prompt
)
from services.ai_services import review_code
import uuid

router = APIRouter(prefix="/assessment", tags=["Assessment"])

sessions = {}

@router.post("/start")
async def start_assessment(req: AssessmentStartRequest):
    session_id = str(uuid.uuid4())
    language = get_language_for_field(req.field)
    prompt = build_assessment_question_prompt(req.field, "beginner")
    question = call_gemini(prompt, {"id", "type", "question", "options", "correct_answer", "explanation", "topic"})
    question["type"] = "mcq"
    sessions[session_id] = {
        "field": req.field,
        "questions": [question],
        "answers": [],
        "current_index": 0,
        "total_questions": 5,
        "original_context": req.user_context.dict(),
        "language": language,
    }
    safe_question = {k: v for k, v in question.items() if k != "correct_answer"}
    return {
        "session_id": session_id,
        "question_number": 1,
        "total_questions": 5,
        "question": safe_question
    }

@router.post("/answer")
async def submit_answer(req: AssessmentAnswerRequest):
    session = sessions.get(req.session_id)
    if not session:
        raise HTTPException(400, "Invalid or expired session")
    current_q = session["questions"][session["current_index"]]
    if current_q["type"] == "mcq":
        is_correct = (req.answer == current_q["correct_answer"])
        session["answers"].append({
            "type": "mcq",
            "question": current_q["question"],
            "user_answer": req.answer,
            "correct": is_correct,
            "topic": current_q["topic"]
        })
    else:  # coding
        code_req = CodeReviewRequest(
            code=req.answer,
            language=session["language"],
            question=current_q["question"],
            user_level="beginner"
        )
        review = await review_code(code_req)
        is_correct = review.get("is_correct", False)
        coding_score = review.get("score", 0)
        session["answers"].append({
            "type": "coding",
            "question": current_q["question"],
            "user_answer": req.answer,
            "correct": is_correct,
            "score": coding_score,
            "topic": "coding"
        })
    session["current_index"] += 1
    if session["current_index"] < 5:
        is_last = (session["current_index"] == 4)
        mcq_answers = [a for a in session["answers"] if a["type"] == "mcq"]
        correct_count = sum(1 for a in mcq_answers if a.get("correct", False))
        if correct_count >= 3:
            next_diff = "advanced"
        elif correct_count >= 1:
            next_diff = "intermediate"
        else:
            next_diff = "beginner"
        if is_last:
            prompt = build_coding_question_prompt(session["field"], next_diff, session["language"], session["answers"])
            next_q = call_gemini(prompt, {"id", "type", "question", "language", "expected_behavior"})
            next_q["type"] = "coding"
        else:
            prompt = build_assessment_question_prompt(session["field"], next_diff, session["answers"])
            next_q = call_gemini(prompt, {"id", "type", "question", "options", "correct_answer", "explanation", "topic"})
            next_q["type"] = "mcq"
        session["questions"].append(next_q)
        sessions[req.session_id] = session
        safe_question = {k: v for k, v in next_q.items() if k != "correct_answer"}
        return {
            "session_id": req.session_id,
            "question_number": session["current_index"] + 1,
            "total_questions": 5,
            "question": safe_question,
            "updated_user_context": None
        }
    # انتهى
    coding_answers = [a for a in session["answers"] if a["type"] == "coding"]
    coding_score_final = coding_answers[0].get("score") if coding_answers else None
    final_prompt = build_assessment_final_prompt(session["field"], session["answers"], coding_score_final)
    result = call_gemini(final_prompt, {"level", "strong_topics", "weak_topics", "summary"})
    original_ctx = UserContext(**session["original_context"])
    original_ctx.level = result["level"]
    original_ctx.strong_topics = result["strong_topics"]
    original_ctx.weak_topics = result["weak_topics"]
    original_ctx.stage = "onboarding"
    mcq_scores = [100 if a.get("correct") else 0 for a in session["answers"] if a["type"] == "mcq"]
    if coding_score_final is not None:
        all_scores = mcq_scores + [coding_score_final]
    else:
        all_scores = mcq_scores
    original_ctx.average_quiz_score = sum(all_scores) / len(all_scores) if all_scores else 0
    del sessions[req.session_id]
    return {
        "session_id": None,
        "question_number": 5,
        "total_questions": 5,
        "question": None,
        "updated_user_context": original_ctx,
        "assessment_summary": result["summary"]
    }