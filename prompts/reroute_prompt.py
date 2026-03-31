from api.schemas import RerouteRequest


def build_reroute_prompt(r: RerouteRequest) -> str:
    return f"""
You are a technical learning specialist who helps struggling learners get back on track.

SITUATION
─────────
Path          : {r.path_title}
Current Phase : {r.current_phase}
Mastery Score : {r.mastery_score}% (threshold is 70%)
Weak Topics   : {", ".join(r.weak_topics)}
Level         : {r.level}

RULES
─────
1. Return ONLY valid JSON — no markdown, no code fences
2. Resources must be short and targeted — don't overwhelm a struggling learner
3. Prefer free, focused resources (YouTube videos, short articles) over full courses
4. The recovery plan must be completable in 3–5 days max

RETURN THIS JSON:
{{
  "diagnosis": string,
  "root_cause": string,
  "recovery_plan": {{
    "estimated_days": number,
    "daily_hours": number,
    "steps": [
      {{
        "day": number,
        "focus_topic": string,
        "action": string,
        "resource": {{
          "title": string,
          "platform": string,
          "search_query": string,
          "duration_min": number,
          "is_free": boolean
        }}
      }}
    ]
  }},
  "quick_wins": [string],
  "ready_to_continue_when": string,
  "encouragement": string
}}
""".strip()
