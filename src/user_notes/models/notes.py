from sqlalchemy import Column, Integer, func, Text, DateTime

from user_notes.database import Base

class Notes(Base):
    __tablename__ = "Notes"

    id = Column(Integer,primary_key=True, index=True)
    title = Column(Text, nullable=False)
    content = Column(Text,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone= True), server_default=func.now(),onupdate=func.now())
