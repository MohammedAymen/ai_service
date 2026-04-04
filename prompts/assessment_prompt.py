def build_assessment_question_prompt(field: str, difficulty: str, previous_answers: list = None) -> str:
    adaptive_hint = ""
    if previous_answers:
        wrong_topics = [a.get("topic") for a in previous_answers if not a.get("correct", False)]
        if wrong_topics:
            adaptive_hint = f"\nركز على المواضيع التي أخطأ فيها: {', '.join(wrong_topics)}."
    return f"""
أنت خبير تقني. أنشئ سؤالاً واحداً من متعدد الخيارات لتقييم مستوى المتعلم في {field}.
الصعوبة: {difficulty}
{adaptive_hint}
يجب أن يكون السؤال عملياً، ليس نظرياً حفظياً.
أعد JSON:
{{
  "id": 1,
  "type": "mcq",
  "question": "السؤال",
  "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
  "correct_answer": "A",
  "explanation": "شرح",
  "topic": "الموضوع"
}}
"""

def build_coding_question_prompt(field: str, difficulty: str, language: str, previous_answers: list = None) -> str:
    adaptive_hint = ""
    if previous_answers:
        wrong_topics = [a.get("topic") for a in previous_answers if not a.get("correct", False)]
        if wrong_topics:
            adaptive_hint = f"\nركز على: {', '.join(wrong_topics)}."
    return f"""
أنت خبير تقني. أنشئ مهمة برمجية عملية بلغة {language} لمتعلم في {field}.
الصعوبة: {difficulty}
{adaptive_hint}
يجب أن تحل المهمة بـ 5-10 أسطر.
أعد JSON:
{{
  "id": 99,
  "type": "coding",
  "question": "وصف المهمة",
  "language": "{language}",
  "expected_behavior": "السلوك المتوقع"
}}
"""

def build_assessment_final_prompt(field: str, answers: list, coding_score: float = None) -> str:
    mcq_answers = [a for a in answers if a.get("type") == "mcq"]
    correct_mcq = sum(1 for a in mcq_answers if a.get("correct", False))
    total_mcq = len(mcq_answers)
    wrong_topics = [a["topic"] for a in mcq_answers if not a.get("correct", False)]
    strong_topics = [a["topic"] for a in mcq_answers if a.get("correct", False)]
    if coding_score is not None:
        final_score = (correct_mcq / total_mcq) * 60 + (coding_score / 100) * 40
    else:
        final_score = (correct_mcq / total_mcq) * 100
    return f"""
بناءً على أداء المتعلم في {field}:
عدد إجابات MCQ الصحيحة: {correct_mcq} من {total_mcq}
درجة البرمجة: {coding_score if coding_score is not None else 'لا توجد'}
النتيجة النهائية المرجحة: {final_score:.1f}%
المواضيع القوية: {strong_topics}
المواضيع الضعيفة: {wrong_topics}

حدد المستوى:
- 80% فأكثر → advanced
- 50% إلى 79% → intermediate
- أقل من 50% → beginner

أعد JSON:
{{
  "level": "beginner|intermediate|advanced",
  "strong_topics": [string],
  "weak_topics": [string],
  "summary": "ملخص قصير (عربي أو إنجليزي)"
}}
"""