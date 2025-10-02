from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.database import Base

class ExamBoard(Base):
    __tablename__ = "exam_board"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    final_grade = Column(String, nullable=False)
    approved_by = Column(Integer, ForeignKey("admins.id"))
    approved_date = Column(DateTime, default=datetime.utcnow)
