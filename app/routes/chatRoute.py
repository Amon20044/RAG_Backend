# app/routers/user.py
from fastapi import APIRouter, File, Form, UploadFile,Path
from app.langchain.main import chat
from app.classes.Classes import Question
from typing import List

chat_router = APIRouter()

@chat_router.post("/{id}", tags=["chat"])
async def chat_endpoint(
    id: str = Path(...),                  
    files: List[UploadFile] = File(None),        
    question: str = Form(...)            
):
    question_input = Question(
        question=question,
        chatId= id,  # <--- use the hashed id here
    )
    response_dict = await chat(question_input, files)
    return response_dict