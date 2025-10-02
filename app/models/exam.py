from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    code = Column(String, nullable=False)
    semester = Column(String, nullable=False)  # Summer/Winter
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
