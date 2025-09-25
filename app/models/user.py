from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, index=True)  # student / teacher / admin
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # later hash this
    department = Column(String, nullable=True)
    student_id = Column(String, unique=True, nullable=True)
    teacher_id = Column(String, unique=True, nullable=True)
