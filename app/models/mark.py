from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Mark(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    score = Column(Integer, nullable=True)
    comments = Column(String, nullable=True)
