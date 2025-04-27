from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class Question(BaseModel):
    question: str
    chatId: str

class Answer(BaseModel):
    answer: str
    question: str

class User(BaseModel):
    email: str
    password: str
    uid: Optional[str] = None  # uid can be a string or None (null)
