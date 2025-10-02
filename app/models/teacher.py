from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    teacher_id = Column(String, unique=True, nullable=False)
    position = Column(String, nullable=True)  # e.g. Professor, Lecturer
    department_id = Column(Integer, ForeignKey("departments.id"))
