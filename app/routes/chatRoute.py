# app/routers/user.py
from fastapi import APIRouter, File, Form, UploadFile,Path, BackgroundTasks
from app.langchain.main import chat
from app.classes.Classes import Question
from typing import List
from app.models.chatModel import save_chat_to_db

chat_router = APIRouter()

@chat_router.post("/{id}", tags=["chat"])
async def chat_endpoint(
    id: str = Path(...),                  
    files: List[UploadFile] = File(None),        
    question: str = Form(...),            
    background_tasks: BackgroundTasks = None # <--- background task support
):
    question_input = Question(
        question=question,
        chatId= id,  # <--- use the hashed id here
    )
    response_dict = await chat(question_input, files)
    background_tasks.add_task(save_chat_to_db, id,response_dict["answer"], response_dict["question"] )
    return response_dict