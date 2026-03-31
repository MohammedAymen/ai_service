from fastapi import FastAPI
from api.routes.ai_routes import router as ai_router

app = FastAPI(title="Smart Learning Platform — AI Service")

app.include_router(ai_router)
