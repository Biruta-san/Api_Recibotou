from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.api.services import chat_service
from app.utils.responses import success_response, error_response, ResponseModel

router = APIRouter(prefix="/chat", tags=["Chatbot"])

# 1. Schema para a pergunta do usuário (o que esperamos receber)
class ChatQuestion(BaseModel):
  question: str

# 2. Schema para a resposta da API (o que enviaremos de volta)
class ChatResponse(BaseModel):
  answer: str

@router.post("/ask", response_model=ResponseModel[ChatResponse], summary="Faz uma pergunta ao chatbot IA.")
async def ask_chatbot(
  request: ChatQuestion,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
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
    return success_response(
      data=ChatResponse(answer=answer),
      message="Categoria criada com sucesso.",
      status_code=status.HTTP_201_CREATED
    )
  except Exception as e:
    return error_response(
      error="Error processing question",
      message="Erro ao processar a pergunta: " + str(e),
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
