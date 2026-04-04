from fastapi import FastAPI
from api.routes.ai_routes import router as ai_router
from api.routes.assessment_routes import router as assessment_router
from api.routes.final_quiz_routes import router as final_quiz_router

app = FastAPI(title="Smart Learning Platform — AI Service")

app.include_router(ai_router)
app.include_router(assessment_router)
app.include_router(final_quiz_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)