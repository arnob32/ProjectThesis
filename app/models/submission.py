from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    attempt_number = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    grade = Column(String, nullable=True)  # Temporary grade before final approval
