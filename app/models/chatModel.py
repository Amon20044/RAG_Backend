from app.db.db import supabase
from typing import List
from app.utils.generateUid import generate_custom_id
def save_chat_to_db(chat_id: str, content: str, question: str):
    Supabase = supabase  # your client

    print(f"Saving chat to DB: {chat_id}, {content}, {question}")

    # 1. Check if chat_id exists in "chats" table
    chat_exists = (
        Supabase
        .table("chats")
        .select("*")
        .eq("chat_id", chat_id)
        .execute()
    )

    # 2. If exists, insert into "messages"
    if chat_exists.data:
        # Chat exists, insert message
        response = (
            Supabase
            .table("messages")
            .insert({
                "message_id": generate_custom_id(),
                "content": content,
                "question": question,
                "chat_id": chat_id
            })
            .execute()
        )
        print(f"Message saved and chatID was already created: {response}")
        return response
    else:
        # 3. If chat_id doesn't exist, create a new chat entry in "chats"
        new_chat = (
            Supabase
            .table("chats")
            .insert({
                "chat_id": chat_id,  # Assuming "chat_id" is a unique identifier for the chat
                "created_at": "now()"  # You can adjust the fields as per your schema
            })
            .execute()
        )


        # Check if the new_chat operation was successful by inspecting `new_chat.data`
        if new_chat.data:  # If there is data in the response, that means the chat was created
            # Now, insert the message after creating the chat
            response = (
                Supabase
                .table("messages")
                .insert({
                    "message_id": generate_custom_id(),
                    "content": content,
                    "question": question,
                    "chat_id": chat_id
                })
                .execute()
            )
            print(f"Message saved and chatID created: {response}")
            return response
        else:
            # Return error if chat creation fails
            return {"error": "Failed to create new chat in chats table. Cannot save message."}
