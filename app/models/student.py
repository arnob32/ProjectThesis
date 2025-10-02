from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # hashed password
    student_id = Column(String, unique=True, nullable=False)  # university roll number
    department_id = Column(Integer, ForeignKey("departments.id"))
