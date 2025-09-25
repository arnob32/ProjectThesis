from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os, shutil, json, base64
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory marks storage (later -> DB)
marks_db = {}

# 🔹 Upload student exam paper
@router.post("/upload/{student_name}")
async def upload_file(student_name: str, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, f"{student_name}.pdf")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "success", "filename": file.filename, "saved_as": f"/static/uploads/{student_name}.pdf"}


# 🔹 Teacher dashboard page
@router.get("/dashboard/teacher", response_class=HTMLResponse)
async def teacher_dashboard(request: Request):
    return templates.TemplateResponse("teacher_dashboard.html", {"request": request})


# 🔹 Student dashboard page
@router.get("/dashboard/student/{student_name}", response_class=HTMLResponse)
async def student_dashboard(request: Request, student_name: str):
    return templates.TemplateResponse("student_dashboard.html", {"request": request, "student_name": student_name})


# 🔹 Generate exam paper
@router.post("/generate-exam", response_class=HTMLResponse)
async def generate_exam(
    request: Request,
    title: str = Form(...),
    code: str = Form(...),
    questions: str = Form(...),
    department: str = Form("general"),
    semester: str = Form("general"),
):
    questions = json.loads(questions)

    file_path = os.path.join(UPLOAD_DIR, f"{department}_{semester}_{code}_exam.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    page_number = 1

    def draw_page_header():
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, height - 2 * cm, title)
        c.setFont("Helvetica", 11)
        c.drawCentredString(width / 2, height - 3 * cm, f"Course Code: {code}")
        c.drawString(2 * cm, height - 4 * cm, "Student Name: _______________________________")
        c.drawString(2 * cm, height - 5 * cm, "Student ID: _________________________________")

    def draw_page_markers():
        margin = 1 * cm
        line_len = 1.5 * cm
        # corners
        c.line(margin, height - margin, margin + line_len, height - margin)
        c.line(margin, height - margin, margin, height - margin - line_len)
        c.line(width - margin, height - margin, width - margin - line_len, height - margin)
        c.line(width - margin, height - margin, width - margin, height - margin - line_len)
        c.line(margin, margin, margin + line_len, margin)
        c.line(margin, margin, margin, margin + line_len)
        c.line(width - margin, margin, width - margin - line_len, margin)
        c.line(width - margin, margin, width - margin, margin + line_len)

    def draw_footer(page_number):
        c.setFont("Helvetica", 9)
        c.drawCentredString(width / 2, 1 * cm, f"Page {page_number}")

    draw_page_header()
    draw_page_markers()
    y = height - 7 * cm

    for idx, q in enumerate(questions, start=1):
        q_text, box_size = q["text"], q["size"]
        c.setFont("Helvetica", 11)
        c.drawString(2 * cm, y, f"Q{idx}: {q_text}")
        y -= 1 * cm

        if box_size == "small":
            box_height = 2 * cm
        elif box_size == "medium":
            box_height = 4 * cm
        else:
            box_height = 6 * cm

        x1, x2 = 2 * cm, width - 2 * cm
        y1, y2 = y - box_height, y
        c.rect(x1, y1, x2 - x1, box_height)
        y = y1 - 2 * cm

        if y < 6 * cm:
            draw_footer(page_number)
            c.showPage()
            page_number += 1
            draw_page_header()
            draw_page_markers()
            y = height - 7 * cm

    draw_footer(page_number)
    c.save()

    pdf_url = f"/static/uploads/{department}_{semester}_{code}_exam.pdf"
    html_content = f"""
    <html>
    <head><title>Exam Preview</title></head>
    <body>
      <h2>Exam Generated: {title} ({code})</h2>
      <p><a href="{pdf_url}" download>⬇ Download PDF</a></p>
      <iframe src="{pdf_url}" width="100%" height="600px"></iframe>
      <br><br>
      <a href="/dashboard/teacher">⬅ Back to Dashboard</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# 🔹 Save annotations
@router.post("/save-annotations/{student}")
async def save_annotations(student: str, payload: dict):
    image_data = payload["image"].split(",")[1]
    file_path = os.path.join(UPLOAD_DIR, f"{student}_annotated.png")
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(image_data))
    return {"status": "success", "file": f"/static/uploads/{student}_annotated.png"}


# 🔹 Save marks and generate graded PDF
@router.post("/save-marks/{student}")
async def save_marks(student: str, marks: dict):
    marks_db[student] = marks
    graded_pdf = os.path.join(UPLOAD_DIR, f"{student}_graded.pdf")
    c = canvas.Canvas(graded_pdf, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 2 * cm, f"Graded Paper for {student}")
    c.setFont("Helvetica", 11)

    # Marks summary
    y = height - 4 * cm
    c.drawString(2 * cm, y, "Marks Summary:")
    y -= 1 * cm
    for q, score in marks.items():
        c.drawString(3 * cm, y, f"{q}: {score}")
        y -= 1 * cm

    # Insert annotation if exists
    ann_path = os.path.join(UPLOAD_DIR, f"{student}_annotated.png")
    if os.path.exists(ann_path):
        img = ImageReader(ann_path)
        c.drawImage(img, 2 * cm, 5 * cm, width=16 * cm, preserveAspectRatio=True, mask="auto")

    c.showPage()
    c.save()

    return {"status": "success", "marks": marks_db[student], "graded_pdf": f"/static/uploads/{student}_graded.pdf"}


# 🔹 Get graded PDF
@router.get("/graded/{student}")
async def get_graded_paper(student: str):
    graded_file = os.path.join(UPLOAD_DIR, f"{student}_graded.pdf")
    if os.path.exists(graded_file):
        return FileResponse(graded_file, media_type="application/pdf", filename=f"{student}_graded.pdf")
    return {"error": "No graded file found"}
