from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.all_models import User, ChatbotHistory
from services.chatbot_service import get_chatbot_response
from pydantic import BaseModel

router = APIRouter(prefix='/chat', tags=['Chatbot'])

class ChatRequest(BaseModel):
    message: str

@router.post('/')
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
        
    response_text = get_chatbot_response(request.message)
    
    new_chat = ChatbotHistory(user_id=user.id, question=request.message, response=response_text)
    db.add(new_chat)
    db.commit()
    
    return {'response': response_text}

@router.get('/history')
def get_chat_history(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        return []
    history = db.query(ChatbotHistory).filter(ChatbotHistory.user_id == user.id).order_by(ChatbotHistory.created_at.desc()).all()
    return history