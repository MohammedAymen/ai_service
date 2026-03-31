from api.schemas import QuizRequest


def build_quiz_prompt(r: QuizRequest) -> str:
    return f"""
You are a technical assessment expert.
Generate a quiz to evaluate understanding of a completed learning unit.

UNIT INFO
─────────
Course : {r.course_title}
Topic  : {r.topic}
Level  : {r.level}

RULES
─────
1. Return ONLY valid JSON — no markdown, no code fences
2. Generate exactly {r.num_questions} MCQ questions
3. Questions must test real understanding, not memorization
4. Include one practical coding/design task at the end
5. Difficulty must match level: {r.level}

RETURN THIS JSON:
{{
  "quiz_title": string,
  "topic": string,
  "level": string,
  "questions": [
    {{
      "id": number,
      "question": string,
      "options": {{ "A": string, "B": string, "C": string, "D": string }},
      "correct_answer": "A" | "B" | "C" | "D",
      "explanation": string,
      "difficulty": "easy" | "medium" | "hard"
    }}
  ],
  "practical_task": {{
    "title": string,
    "description": string,
    "expected_output": string,
    "estimated_minutes": number,
    "evaluation_criteria": [string]
  }},
  "passing_score": number
}}
""".strip()
