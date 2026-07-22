from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(200), nullable=False)
    comment = Column(Text, nullable=False)
    ai_category = Column(String(100), nullable=True)
    ai_sentiment = Column(String(50), nullable=True)
    ai_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
