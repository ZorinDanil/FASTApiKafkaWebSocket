import json
from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, HTTPException
from typing import List
from app.core.database import get_database
from app.models.chat import Chat
from app.models.message import Message
from app.core.security import auth_validator
from app.websocket.manager import manager
from app.schemas.chat import ChatCreate

router = APIRouter(tags=["Chats"])


@router.post("/", response_model=Chat)
async def create_chat(chat_data: ChatCreate, token: str, db=Depends(get_database)):
    """
    Create a new chat.

    Args:
        chat_data (ChatCreate): The data required to create a chat.
        token (str): The authentication token.

    Returns:
        Chat: The created chat object.
    """
    user_id = await auth_validator.validate_token(token)
    participants = list(set(chat_data.participants + [user_id]))
    participants.sort()
    chat = Chat(participants=participants)
    await db["chats"].insert_one(chat.dict())
    return chat


@router.get("/", response_model=List[Chat])
async def get_chat_by_participants(participants: str, token: str, db=Depends(get_database)):
    """
    Retrieve chats by participants.

    Args:
        participants (str): Comma-separated participant IDs.
        token (str): The authentication token.

    Returns:
        List[Chat]: A list of chat objects.
    """
    user_id = await auth_validator.validate_token(token)
    participants_list = sorted(participants.split(",") + [user_id])
    chat_cursor = db["chats"].find({"participants": participants_list})
    chats = await chat_cursor.to_list(length=None)
    if not chats:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chats


@router.post("/messages/", response_model=Message)
async def send_message(chat_id: str, content: str, token: str, db=Depends(get_database)):
    """
    Send a message to a chat.

    Args:
        chat_id (str): The ID of the chat.
        content (str): The content of the message.
        token (str): The authentication token.

    Returns:
        Message: The sent message object.
    """
    user_id = await auth_validator.validate_token(token)
    message = Message(chat_id=chat_id, sender_id=user_id, content=content)
    await db["messages"].insert_one(message.dict())
    await db["chats"].update_one({"_id": chat_id}, {"$push": {"messages": message.id}})
    await manager.broadcast(json.dumps(message.dict()))
    return message


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str, token: str, db=Depends(get_database)):
    """
    WebSocket endpoint for real-time chat communication.

    Args:
        chat_id (str): The ID of the chat.
        token (str): The authentication token.
    """
    user_id = await auth_validator.validate_token(token)
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message_data["sender_id"] = user_id
            message_data["chat_id"] = chat_id
            message = Message(**message_data)
            await db["messages"].insert_one(message.dict())
            await db["chats"].update_one({"id": chat_id}, {"$push": {"messages": message.id}})
            await manager.broadcast(json.dumps(message.dict()))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")


@router.get("/{chat_id}/messages", response_model=List[Message])
async def get_chat_messages(chat_id: str, token: str = Query(...), db=Depends(get_database)):
    """
    Retrieve messages from a chat.

    Args:
        chat_id (str): The ID of the chat.
        token (str): The authentication token.

    Returns:
        List[Message]: A list of message objects.
    """
    user_id = await auth_validator.validate_token(token)
    chat = await db["chats"].find_one({"id": chat_id, "participants": user_id})
    if not chat:
        raise HTTPException(status_code=403, detail="You are not a participant of this chat")
    messages_cursor = db["messages"].find({"chat_id": chat_id})
    messages = await messages_cursor.to_list(length=None)
    return messages
