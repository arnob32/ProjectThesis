from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Routers
from app.routes import auth_routes, dashboard_routes

# Database
from app.database import Base, engine

# Import models so Base knows them
from app.models import user
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.admin import Admin
from app.models.department import Department
from app.models.exam import Exam
from app.models.submission import Submission
from app.models.mark import Mark
from app.models.exam_board import ExamBoard

# ✅ Create all database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# ✅ Serve static files (PDFs, CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ✅ Include routes
app.include_router(auth_routes.router)
app.include_router(dashboard_routes.router)
