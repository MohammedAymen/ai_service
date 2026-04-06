from services.code_executor import run_code
from api.schemas import (
    LearningPathRequest,
    QuizRequest,
    WeeklyReportRequest,
    RerouteRequest,
    ChatRequest,
    CodeReviewRequest,
)
from prompts.learning_path_prompt import build_learning_path_prompt
from prompts.quiz_prompt import build_quiz_prompt
from prompts.weekly_report_prompt import build_weekly_report_prompt
from prompts.reroute_prompt import build_reroute_prompt
from prompts.chat_prompt import build_chat_prompt
from prompts.code_review_prompt import build_code_review_prompt
from core.gemini_client import call_gemini, call_gemini_chat

def generate_learning_path(r: LearningPathRequest) -> dict:
    return call_gemini(
        prompt=build_learning_path_prompt(r),
        required_keys={"meta", "phases", "weekly_schedule", "overall_milestones"},
    )


def generate_quiz(r: QuizRequest) -> dict:
    return call_gemini(
        prompt=build_quiz_prompt(r),
        required_keys={"questions", "practical_task", "passing_score"},
    )


def generate_weekly_report(r: WeeklyReportRequest) -> dict:
    return call_gemini(
        prompt=build_weekly_report_prompt(r),
        required_keys={"overall_status", "recommendations", "next_week_focus"},
    )


def generate_reroute(r: RerouteRequest) -> dict:
    return call_gemini(
        prompt=build_reroute_prompt(r),
        required_keys={"diagnosis", "recovery_plan", "ready_to_continue_when"},
    )


def generate_chat_reply(r: ChatRequest) -> dict:
    return call_gemini_chat(build_chat_prompt(r))


async def review_code(r: CodeReviewRequest) -> dict:
    execution_result = await run_code(r.code, r.language)

    review = call_gemini(
        prompt=build_code_review_prompt(r, execution_result),
        required_keys={"is_correct", "score", "feedback"},
    )

    review["execution"] = execution_result

    return review
