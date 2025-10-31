# app/api/routers/chat.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.api.services import chat_service

router = APIRouter(prefix="/chat", tags=["Chatbot"])

# 1. Schema para a pergunta do usuário (o que esperamos receber)
class ChatQuestion(BaseModel):
  question: str

# 2. Schema para a resposta da API (o que enviaremos de volta)
class ChatResponse(BaseModel):
  answer: str

@router.post("/ask", response_model=ChatResponse)
async def ask_chatbot(
  request: ChatQuestion,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_active_user)
):
  """
  Recebe uma pergunta do usuário, processa com o serviço de IA e retorna a resposta.
  """
  try:
    # Chama nosso serviço orquestrador, passando o ID do usuário para que ele busque os dados corretos
    answer = await chat_service.ask_question(
      db=db,
      user_id=current_user.id,
      question=request.question
    )
    return ChatResponse(answer=answer)
  except Exception as e:
    # Se qualquer erro acontecer no serviço, retornamos um erro 500 genérico e seguro
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Ocorreu um erro inesperado ao processar sua pergunta: {e}"
    )
