from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime

class ContactBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=20)
    comment: str = Field(..., min_length=1, max_length=2000)

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Имя не может быть пустым')
        return v.strip()

    @validator('comment')
    def validate_comment(cls, v):
        if not v.strip():
            raise ValueError('Комментарий не может быть пустым')
        return v.strip()

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    ai_category: Optional[str] = Field(default=None, max_length=100)
    ai_sentiment: Optional[str] = Field(default=None, max_length=50)
    ai_response: Optional[str] = Field(default=None)

class ContactResponse(ContactBase):
    id: int
    ai_category: Optional[str]
    ai_sentiment: Optional[str]
    ai_response: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
