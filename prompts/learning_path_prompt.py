from core.config import SUPPORTED_FIELDS
from api.schemas import LearningPathRequest


def build_learning_path_prompt(r: LearningPathRequest) -> str:
    return f"""
You are a world-class technical learning architect.
Supported fields ONLY: {", ".join(SUPPORTED_FIELDS)}.

LEARNER PROFILE
───────────────
Goal         : {r.goal}
Field        : {r.field}
Level        : {r.level}
Background   : {r.background}
Hours/Day    : {r.hours_per_day}
Language     : {r.language}
Target       : {r.target_months} months

RULES
─────
1. Return ONLY valid JSON — no markdown, no code fences
2. Total hours must match: {r.hours_per_day} hrs/day × ~5 days × total_weeks
3. All courses must be real and searchable
4. Language: Arabic → prefer Arabic | Both → 60% Arabic, 40% English
5. Prefer free resources over paid when quality is equal

RETURN THIS JSON:
{{
  "meta": {{
    "path_title": string,
    "field": string,
    "total_weeks": number,
    "total_hours": number,
    "progression": string
  }},
  "phases": [
    {{
      "phase_number": number,
      "phase_title": string,
      "week_start": number,
      "week_end": number,
      "objective": string,
      "courses": [
        {{
          "id": string,
          "title": string,
          "instructor": string,
          "platform": string,
          "search_query": string,
          "estimated_hours": number,
          "is_free": boolean,
          "topics": [string],
          "why_this_course": string
        }}
      ],
      "milestones": [
        {{
          "title": string,
          "type": "project" | "skill" | "knowledge",
          "how_to_verify": string
        }}
      ],
      "project": {{
        "title": string,
        "description": string,
        "estimated_hours": number,
        "deliverable": string
      }}
    }}
  ],
  "weekly_schedule": {{
    "hours_per_day": number,
    "days_per_week": number,
    "daily_breakdown": {{
      "theory_min": number,
      "practice_min": number,
      "review_min": number
    }},
    "weekly_plan": [
      {{ "day": string, "focus": string, "duration_hrs": number }}
    ]
  }},
  "overall_milestones": [
    {{ "week": number, "title": string, "description": string }}
  ],
  "success_metrics": {{
    "weekly_checks": [string],
    "phase_gates": [string],
    "final_outcome": string
  }},
  "adaptation_tips": [string]
}}
""".strip()
