from api.schemas import WeeklyReportRequest


def build_weekly_report_prompt(r: WeeklyReportRequest) -> str:
    avg_score = sum(r.quiz_scores) / len(r.quiz_scores) if r.quiz_scores else 0
    completion_rate = (r.hours_studied / r.target_hours * 100) if r.target_hours else 0

    return f"""
You are a supportive and honest learning coach.
Analyze this learner's weekly performance and generate a personalized report.

WEEK {r.week_number} STATS
──────────────────
Path           : {r.path_title}
Topics Done    : {", ".join(r.completed_topics)}
Quiz Scores    : {r.quiz_scores} → Average: {avg_score:.1f}%
Hours Studied  : {r.hours_studied} / {r.target_hours} target ({completion_rate:.0f}% completion)
Struggles      : {r.struggles or "None reported"}

RULES
─────
1. Return ONLY valid JSON — no markdown, no code fences
2. Be honest but encouraging — highlight real strengths AND real gaps
3. Recommendations must be specific and actionable, not generic
4. Tone: like a mentor who genuinely cares about the learner's progress

RETURN THIS JSON:
{{
  "week_number": number,
  "overall_status": "on_track" | "slightly_behind" | "at_risk",
  "summary": string,
  "strengths": [string],
  "gaps": [string],
  "recommendations": [
    {{
      "priority": "high" | "medium" | "low",
      "action": string,
      "reason": string
    }}
  ],
  "next_week_focus": string,
  "motivational_note": string,
  "adjusted_pace_needed": boolean,
  "suggested_adjustment": string
}}
""".strip()
