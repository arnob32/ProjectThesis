# 📚 Exam Grading System

An academic project to digitalize exam grading for universities.  
Built with **FastAPI**, **SQLite**, and a **modern HTML/CSS/JS frontend**.

---

## ✨ Features
- 🔐 Authentication for Students, Teachers, and Admin
- 📝 Teacher Dashboard: create exams, upload submissions, grade papers
- 🎓 Student Dashboard: view results, download feedback
- 🛠️ Admin Dashboard: manage users, oversee system
- 📂 File Uploads: teachers upload annotated exam PDFs
- 📊 Database Storage: SQLite for users, exams, submissions, marks

## 📂 Project Structure
PROJECTTHESIS/
│── app/
│ ├── models/ # SQLAlchemy models (User, Exam, Submission, Mark)
│ ├── routes/ # API routes (auth, dashboard, exams, uploads)
│ ├── schemas/ # Pydantic schemas
│ ├── services/ # Business logic
│ ├── static/ # Static files (uploads, assets)
│ ├── templates/ # HTML templates (dashboards, auth pages)
│ ├── database.py # DB connection
│ ├── main.py # FastAPI entry point
│── tests/ # Future unit tests
│── app.db # SQLite database
│── requirements.txt # Python dependencies
│── README.md # Documentation


---

## 🚀 Getting Started

### 1. Clone the Repository

git clone <your-repo-link>
cd PROJECTTHESIS

### 1.2  Create Virtual Environment

python -m venv myenv
source myenv/bin/activate   # Linux/Mac
myenv\Scripts\activate      # Windows 

### 1.3 Install Dependencies

pip install -r requirements.txt


### 1.4 Run Server

uvicorn app.main:app --reload
Visit the app at: http://127.0.0.1:8000



### 2. 🗄️ Database
Uses SQLite (app.db)

Tables:

users → Students, Teachers, Admins

exams → Created by teachers

submissions → Student uploads

marks → Teacher feedback & scores

📌 You can explore the DB inside VS Code with the SQLite Explorer extension.


### 3. 📊 UML Diagrams
Class Diagram

(insert your UML image here)

Use Case Diagram

(insert your use case UML here)




### 4.📸 Screenshots

Teacher dashboard

Student dashboard

Exam creation page

Annotated exam PDF preview


### 5.🔮 Future Improvements

AI-based auto-grading

Cloud deployment (AWS/Azure/GCP)

Notifications (email/SMS)

Rich analytics dashboards


### 6.👨‍💻 Author
Your Name

University / Department

Contact: your.email@university.edu





