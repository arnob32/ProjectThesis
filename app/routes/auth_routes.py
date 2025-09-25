from fastapi import APIRouter, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ---------------------------
# 🔹 AUTH PAGES (UI)
# ---------------------------
@router.get("/auth", response_class=HTMLResponse)
def auth_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


# ---------------------------
# 🔹 SIGNUP
# ---------------------------
@router.post("/auth/signup", response_model=UserResponse)
def signup(
    role: str = Form(...),
    department: str = Form(...),
    subject: str = Form(None),
    student_id: str = Form(None),
    position: str = Form(None),
    teacher_id: str = Form(None),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    # Check if email already exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        role=role,
        department=department,
        student_id=student_id,
        teacher_id=teacher_id,
        email=email,
        password=password,  # TODO: hash before storing!
        name=email.split("@")[0],  # simple default
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ---------------------------
# 🔹 LOGIN
# ---------------------------
@router.post("/auth/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user": {"id": user.id, "role": user.role}}


# ---------------------------
# 🔹 PRINT USERS (debug)
# ---------------------------
@router.get("/auth/print-users")
def print_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    print("📋 Current Users in DB:", flush=True)
    for u in users:
        print(f"ID={u.id}, Email={u.email}, Role={u.role}", flush=True)
    return {"count": len(users), "status": "printed in terminal"}


# ---------------------------
# 🔹 DASHBOARDS
# ---------------------------
@router.get("/dashboard/student", response_class=HTMLResponse)
def student_dashboard(request: Request):
    return templates.TemplateResponse("student_dashboard.html", {"request": request})


@router.get("/dashboard/teacher", response_class=HTMLResponse)
def teacher_dashboard(request: Request):
    return templates.TemplateResponse("teacher_dashboard.html", {"request": request})
