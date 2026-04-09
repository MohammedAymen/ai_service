# 📘 Smart Learning Platform – API Documentation

>اول حاجه المفروض نتكلم عنها هي السيناريو اللي هنمشي عليه طول الابليكيشن اول حاجه الشخص هيخش الابليكيشن هيحط الداتا بتاعته (الاسم - الايميل - التراك - المستوى -الهدف بتاعه- عدد ساعات المذاكره) بعدين الداتا دي هنستعملها في المرحله الاولى بس قبل المرحله الاولى لازم اعرفك على حاجه الاول

---

## 🧠 Overview

- النظام Stateless
- الـ Frontend مسؤول عن تخزين user_context
- كل Endpoint ممكن يرجع updated_user_context
- لازم يتم دمج التحديثات بعد كل Request

---

## 📦 UserContext
دي الداتا الاساسيه بتاعت كل شخص المفروض تتحفظ عندك 
```json
{
  "name": "string *",
  "goal": "string",
  "field": "string *",
  "level": "beginner | intermediate | advanced *",
  "started_at": "string (ISO date)",
  "stage": "assessment | onboarding | learning | recovery",
  "path_title": "string",
  "total_phases": 0,
  "current_phase_number": 0,
  "current_phase_title": "string",
  "current_course_title": "string",
  "current_course_url": "string",
  "completed_phases": [],
  "completed_topics": [],
  "remaining_topics": [],
  "overall_progress_percent": 0.0,
  "quiz_scores": [],
  "average_quiz_score": 0.0,
  "strong_topics": [],
  "weak_topics": [],
  "hours_per_day": 0.0,
  "hours_studied_this_week": 0.0,
  "target_hours_this_week": 0.0,
  "total_hours_studied": 0.0,
  "struggles": "string",
  "last_activity": "string (ISO datetime)"
}
```

---

# 🚀 API Endpoints
نخش هنا بقى على كل كل اند بوين موجوده في الاب اول حاجه هنخش عليها وهي 
## 1️⃣ Assessment
دي متقسمه لحاجتين يا بدايه الاسايمنت وهنا انت بتعتي الداتا اللي تحت ويرجعلك السؤال وبعدها هتحطي الاجابه في الشكل ده وفي الاخر هيقولك صح ولا غلط 
### POST /assessment/start

| Field | Type | Required |
|------|------|--------|
| user_context | object | Yes |
| field | string | Yes |
| goal | string | No |
#### Request Body
```json
{
 "user_context": "UserContext"
    "field": "str"
    "goal": str = ""
}
```
بالشكل ده وهيرجهلك الشكل ده 
#### Response 
```json
{
  "session_id": "uuid",
  "question_number": 1,
  "total_questions": 5,
  "question": {
    "id": 1,
    "type": "mcq",
    "question": "نص السؤال",
    "options": { "A": "...", "B": "...", "C": "...", "D": "..." },
    "explanation": "شرح",
    "topic": "الموضوع"
  }
  ```
دي الداتا اللي هترجعلك السؤال بالاختيارات ولو الشخص طلب شرح بتبعتيله الشرح 
---

### POST /assessment/answer
هنا بقى لما يجاوب الشخص هتبعتيله الداتا دي على الراوت دي بالشكل ده 
| Field | Type |
|------|------|
| session_id | string |
| answer | string |
#### Request Body
```json
{
 "session_id": str
    "answer": str
}
```
هو فوق بيبعتلك رقم عشوائي وهو رقم السيشن فا هتبعتيها مع الاجابه بتاعت الشخص وهيرجعلك كدا 
#### Response 
```json
{
  "session_id": "نفسه",
  "question_number": 2,
  "total_questions": 5,
  "question": { /* السؤال التالي */ },
  "updated_user_context": null
}
```
والرد على نهاية الامتحان هيكون كدا 
#### Response 
```json
{
  "session_id": null,
  "question_number": 5,
  "total_questions": 5,
  "question": null,
  "updated_user_context": { /* كامل UserContext جديد مع تحديث level, strong_topics, weak_topics, stage="onboarding" */ },
  "assessment_summary": "ملخص النتيجة"
}
```
هنخش على السؤال التاني وفي الاخر خالص لما نخلص هيديلك التقييم النهائي للشخص سواء هو بيزك او متوسط او ادفانسد 
وبعدين يبعتلك النقط القوة والضعف والكلام ده كله المهم انت هتحتفظي بداتا المستوى علشان نخش على المرحله اللي بعد كدا 
وهي الرود ماب 
---

## 2️⃣ Learning Path
انت هنا هتبعتي على الراوت ده بعد ما يخلص الامتحان الداتا اللي تحت علشان يولد الرود ماب 
### POST /ai/learning-path

| Field | Type |
|------|------|
| goal | string |
| field | string |
| level | string |
| hours_per_day | float |
#### Request Body
```json
{
    "goal": str,            
    "field": str,         
    "level": Literal,
    "background": str,      
    "hours_per_day": float, 
    "language": Literal,
    "target_months": int   
}
```
تمام والرد اللي هيجيلك من هنا هيبقى على الشكل ده 
#### Response 
```json
{
  "status": "success",
  "data": {
    "meta": { "path_title": "...", "total_weeks": 24, ... },
    "phases": [ /* قائمة المراحل */ ],
    "weekly_schedule": { ... },
    "overall_milestones": [ ... ]
  }
  ```
}
بعد ما تخلصي حوار الرود ماب وتخزينيها عندك هنخش على المرحله التانيه وهي انك تبعتي الرود ماب للشات علشان يشرحلها للمستخدم ويبقى معاه يعني خطوة خطوة 
---

## 3️⃣ AI Chat
هنا هنخش على الشات وهتبعتي للشات اول مره على الراوت ده الداتا دي علشان يشرح للشخص الرود ماب ويبقى معاه اول باول 
### POST /ai/chat

| Field | Type |
|------|------|
| message | string |
| user_context | object |
| chat_history | array |
مثال عملي مثلا 
#### Request Body
```json{
  "message": "شرح لي الرود ماب بتاعتي وأول كورس",
  "user_context": {
    "name": "محمد",
    "goal": "أريد أن أصبح مطور واجهات أمامية",
    "field": "Web Development",
    "level": "beginner",
    "stage": "onboarding",
    "path_title": "Professional Front-End Developer Roadmap (6-Month Mastery)",
    "total_phases": 4,
    "current_phase_number": 1,
    "current_phase_title": "Modern Styling & Responsive Design",
    "current_course_title": "HTML & CSS Mastery 2021",
    "current_course_url": "https://www.youtube.com/results?search_query=Elzero+Web+School+HTML+CSS+2021",
    "completed_phases": [],
    "overall_progress_percent": 0.0,
    "strong_topics": [],
    "weak_topics": [],
    "hours_per_day": 2,
    "hours_studied_this_week": 10,
    "target_hours_this_week": 10,
    "total_hours_studied": 30,
    "last_activity": "2026-04-04T12:00:00"
  },
  "chat_history": [
    {
      "role": "user",
      "content": "مرحباً، أنا جديد هنا"
    },
    {
      "role": "assistant",
      "content": "أهلاً بك! كيف يمكنني مساعدتك في رحلة التعلم؟"
    }
  ]

}
```
ده بيبقى الشكل بتاع الماسد اللي هتتبعت ولما تبعتيها هيرجعلك ماسدج شكلها كدا 
#### Response 
```json
{
  "status": "success",
  "data": {
    "type": "info | course | question | congrats | feedback",
    "message": "نص الرد",
    "data": { "title": "...", "url": "...", "platform": "...", "estimated_hours": 0 },
    "updated_user_context": { /* قد يكون null */ }
  },
  "updated_user_context": { /* نفس الحقل */ }
}
```
يخزنه العميل: إذا وُجد updated_user_context، يدمجه مع user_context. يضيف الرسالة والرد إلى chat_history.
وبتعملي ابديت 
وبكدا هتبعتي اخر 10 ماسدجات في الشات مع الهيستوري وبكدا المستخدم لو حب يسأل في نص الماسدج عادي 
---

## 4️⃣ Quiz
هنا الامتحان اللي بيتعمل اللي لسه هضيفه ده اللي هيتعمل في نص الكورس 
### POST /ai/quiz

| Field | Type |
|------|------|
| topic | string |
| level | string |
| num_questions | int |
#### Request Body
```json
{
"course_title": str  = Field(..., example="Python for Everybody")
    "topic": str         = Field(..., example="Functions and Recursion")
    "level": Literal["beginner", "intermediate", "advanced"] = "beginner"
    "num_questions": int = Field(default=5, ge=3, le=10)
}
```
هتبعيله داتا شكلها كدا وهتاخدي داتا شكلها كدا 
#### Response 
```json
{
  "status": "success",
  "data": {
    "quiz_title": "...",
    "questions": [
      {
        "id": 1,
        "question": "...",
        "options": { "A": "...", "B": "...", "C": "...", "D": "..." },
        "correct_answer": "B",
        "explanation": "...",
        "difficulty": "easy"
      }
    ],
    "practical_task": { ... },
    "passing_score": 2
  }
}
```
انا لسه مضيفتش جزئيه الحل لسه هعملها 
---
## ✅ Quiz Evaluation (NEW)

### POST /quiz/submit
Evaluates quiz answers and returns detailed feedback.
#### Request Body
{
  "answers": { "1": "B", "2": "C", "3": "A" },
  "questions": [],
  "passing_score": 66,
  "language": "Arabic"
}
#### Response
{
  "score": 2,
  "total": 3,
  "percentage": 66.7,
  "passed": false,
  "passing_score": 66,
  "results": [
    {
      "id": 1,
      "question": "...",
      "user_answer": "B",
      "correct_answer": "B",
      "is_correct": true,
      "explanation": "...",
      "topic": "CSS Grid"
    }
  ],
  "summary": "...",
  "recommendation": "..."
}
### Notes:
- لا يتم استخدام `session_id` لأن التصحيح يعتمد على البيانات المرسلة بالكامل.
- الـ Frontend مسؤول عن عرض النتيجة للمستخدم.
- يتم تخزين النتائج مؤقتًا (Local State أو LocalStorage).
- يدعم النظام Feedback ذكي من خلال `summary` و `recommendation`.

## 5️⃣ Final Quiz
ده فاينل كويز بيبقى في نهاية كل كورس بتناديه بتنادي استارت اول حاجه 
### POST /final-quiz/start
هتدي داتا شكلها كدا 
#### Request Body
```json
{
  "user_context": {
    "name": "محمد",
    "goal": "أريد أن أصبح مطور واجهات أمامية",
    "field": "Web Development",
    "level": "beginner",
    "stage": "learning",
    "path_title": "Professional Front-End Developer Roadmap (6-Month Mastery)",
    "total_phases": 4,
    "current_phase_number": 1,
    "current_phase_title": "Modern Styling & Responsive Design",
    "current_course_title": "HTML & CSS Mastery 2021",
    "current_course_url": "https://www.youtube.com/results?search_query=Elzero+Web+School+HTML+CSS+2021",
    "completed_phases": [],
    "overall_progress_percent": 0.0,
    "strong_topics": [],
    "weak_topics": [],
    "hours_per_day": 2,
    "hours_studied_this_week": 10,
    "target_hours_this_week": 10,
    "total_hours_studied": 30,
    "last_activity": "2026-04-04T12:00:00"
  }
}
```
وبترجعلك داتا شكلها كدا 
#### Response 
```json
{
  "session_id": "uuid",
  "quiz_title": "...",
  "questions": [
    {
      "id": 1,
      "question": "...",
      "options": { "A": "...", "B": "...", "C": "...", "D": "..." },
      "explanation": "...",
      "difficulty": "easy"
    }
  ],
  "practical_task": { ... },
  "passing_score": 70
}
```
برضوا زي امتحان تحديد المستوى في سيشن هتحطيه مع الراوت الجايه 
### POST /final-quiz/submit
هنا هتحطي داتا شكلها كدا 
#### Request Body
```json
{
  "session_id": "456d6634-416a-4261-8394-7110241d2137",
  "answers": {
    "1": "B",
    "2": "C",
    "3": "B",
    "4": "C",
    "5": "B",
    "6": "B",
    "7": "B",
    "8": "C",
    "9": "B",
    "10": "A"
  },
  "user_context": {
    "name": "محمد",
    "goal": "أريد أن أصبح مطور واجهات أمامية",
    "field": "Web Development",
    "level": "beginner",
    "stage": "learning",
    "path_title": "Professional Front-End Developer Roadmap (6-Month Mastery)",
    "total_phases": 4,
    "current_phase_number": 1,
    "current_phase_title": "Modern Styling & Responsive Design",
    "current_course_title": "HTML & CSS Mastery 2021",
    "current_course_url": "https://www.youtube.com/results?search_query=Elzero+Web+School+HTML+CSS+2021",
    "completed_phases": [],
    "overall_progress_percent": 0.0,
    "strong_topics": [],
    "weak_topics": [],
    "hours_per_day": 2,
    "hours_studied_this_week": 10,
    "target_hours_this_week": 10,
    "total_hours_studied": 30,
    "last_activity": "2026-04-04T12:00:00"
  }
}
```
(session-id ده بيجي مع كل ريكويست وبيتمسح بعدها علطول فلو اتعمل سابمت مرتين ورا بعض هيحصل ايرور)
وهترد عليها بقى برد شكله كدا 
#### Response 
```json
{
  "passed": true,
  "score": 100.0,
  "passing_score": 70,
  "updated_user_context": { /* كامل UserContext مع تحديث current_phase_number, completed_phases, overall_progress_percent */ },
  "message": "تهانينا! اجتزت الاختبار..."
}
```
وبكدا الشخص يكون عدا الاختبار هو الليميت بتاع 70% لو جاب اقل هيتعمله اعاده تقييم انما لو اعلى بكدا هو نجح ودخل على الفيز التانيه الا وهي معاكي يا هتجيبيها من الداتا اللي معاكي يا هتبعتيها للشات مره تانيه علشان يخش على الفيز التانيه ويبعتلك اللينك بتاع الكورس 
---

## 6️⃣ Reroute
هنا لو جاب اقل من 70% في الامتحان بيتعمله اعاده تقييم ويعرف هو وقع في ايه ويقترحله كورسات هو وقع فيها
### POST /ai/reroute
#### Request Body
``` json
{
  "path_title": "Professional Front-End Developer Roadmap (6-Month Mastery)",
  "current_phase": "Modern Styling & Responsive Design",
  "mastery_score": 45.0,
  "weak_topics": ["CSS Grid", "Flexbox", "Media Queries"],
  "level": "beginner"
}
```
وهيرجعلك ده 
#### Response 
``` json
{
  "status": "success",
  "data": {
    "diagnosis": "...",
    "recovery_plan": { ... },
    "ready_to_continue_when": "...",
    "encouragement": "..."
  }
}
```
---

## 7️⃣ Weekly Report
نخش بقى على جزئيه التقييم الاسبوعي
### POST /ai/weekly-report
#### Request Body
```json
{
  "week_number": 3,
  "path_title": "Professional Front-End Developer Roadmap (6-Month Mastery)",
  "completed_topics": ["HTML Basics", "CSS Intro", "Flexbox"],
  "quiz_scores": [85, 70, 95],
  "hours_studied": 12.5,
  "target_hours": 15.0,
  "struggles": "ما زلت أجد صعوبة في فهم CSS Grid وترتيب العناصر المعقدة."
}
```
هيرجعلك الداتا دي 
#### Response 
```json
{
  "status": "success",
  "data": {
    "overall_status": "on_track | slightly_behind | at_risk",
    "summary": "...",
    "recommendations": [ { "priority": "high", "action": "...", "reason": "..." } ],
    "next_week_focus": "...",
    "motivational_note": "..."
  }
}
```
---

## 8️⃣ Code Review
هنا بقى جزئيه الكود ريفيو لو الشخص بعت كود مثلا او في سؤال في كودين او اي حاجه من الحاجات دي يبقى هنروح للراوت دي 
### POST /ai/code-review
#### Request Body
```json
{
  "code": "function sumEvenNumbers(arr) {\n  let sum = 0;\n  for (let i = 0; i < arr.length; i++) {\n    if (arr[i] % 2 === 0) {\n      sum += arr[i];\n    }\n  }\n  return sum;\n}",
  "language": "javascript",
  "question": "اكتب دالة تحسب مجموع الأعداد الزوجية في مصفوفة أرقام.",
  "user_level": "beginner"
}
```
بالشكل ده بيتبعت الكود هيتم عمل رن ليه وهيتبعتلك الناتج ده 
#### Response 
```json
{
  "status": "success",
  "data": {
    "is_correct": true,
    "score": 95,
    "execution": { "stdout": "", "stderr": "", "language": "javascript", "version": "18.15.0" },
    "feedback": { "summary": "...", "what_is_good": "...", "how_to_improve": "..." }
  }
}
```
بيرجعلك كل اللي احنا محتاجينه من تقييم الكود وايه التحسينات وكل الكلام ده 
---

# 🔄 Data Flow

| Step | Action | Storage |
|------|--------|--------|
| Start | Create user_context | LocalStorage |
| After Assessment | Update context | Replace |
| After Roadmap | Save phases | Store |
| Chat | Update history | Append |
| Final Quiz | Update progress | Merge |

