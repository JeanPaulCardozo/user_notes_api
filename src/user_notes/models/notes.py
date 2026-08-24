from sqlalchemy import Column, Integer, func, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from user_notes.database import Base


class Notes(Base):
    __tablename__ = "Notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    owner_id = Column(Integer, ForeignKey("Users.id"), nullable=False)

    owner = relationship("User")