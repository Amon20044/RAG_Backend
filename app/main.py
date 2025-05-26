from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chatRoute import chat_router  # Correct import
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat", tags=["chat"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use "PORT" as the environment variable key
    uvicorn.run(app, host="0.0.0.0", port=port)  # To ensure it's accessible from external sources
