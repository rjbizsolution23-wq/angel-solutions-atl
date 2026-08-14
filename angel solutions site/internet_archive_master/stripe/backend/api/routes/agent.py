"""
Agent interaction endpoints.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.agent_engine import create_agent
from services.supabase_service import get_supabase_service
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    conversation_id: str
    success: bool


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Chat with the Stripe AI agent.
    
    Args:
        request: Chat request with message and optional conversation_id
    
    Returns:
        Agent response with conversation_id
    """
    try:
        # Create or retrieve conversation
        conversation_id = request.conversation_id
        if not conversation_id:
            supabase = get_supabase_service()
            conversation = supabase.create_conversation()
            conversation_id = conversation.get("id")
        
        # Create agent and process message
        agent = create_agent(conversation_id=conversation_id)
        result = await agent.process_message(request.message)
        
        return ChatResponse(
            response=result["response"],
            conversation_id=conversation_id,
            success=result["success"]
        )
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: str):
    """Get all messages for a conversation."""
    try:
        supabase = get_supabase_service()
        messages = supabase.get_conversation_messages(conversation_id)
        return {"messages": messages}
    except Exception as e:
        logger.error(f"Error retrieving messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/actions")
async def get_agent_actions(conversation_id: Optional[str] = None, limit: int = 50):
    """Get agent action audit log."""
    try:
        supabase = get_supabase_service()
        actions = supabase.get_agent_actions(conversation_id=conversation_id, limit=limit)
        return {"actions": actions}
    except Exception as e:
        logger.error(f"Error retrieving actions: {e}")
        raise HTTPException(status_code=500, detail=str(e))
