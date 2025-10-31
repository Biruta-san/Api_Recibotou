from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.api.services import analysis_service
from app.utils.responses import success_response, error_response, ResponseModel

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/monthly_summary", response_model=ResponseModel[dict])
async def get_monthly_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    year: int = date.today().year,
    month: int = date.today().month,
):
  """
  Retorna o resumo financeiro (Receitas, Despesas, Saldo) para o mês/ano especificados.
  """
  try:
    # Chama o serviço que criamos, passando o ID do usuário logado
    summary = analysis_service.get_monthly_summary(
      db=db,
      user_id=current_user.id,
      year=year,
      month=month
    )

    return success_response(
      data=summary,
      message=f"Resumo para {month}/{year} calculado com sucesso."
    )
  except Exception as e:
    # Em caso de erro na lógica do serviço, retornamos um 500
    raise HTTPException(
        status_code=500,
        detail=f"Erro interno ao calcular o resumo: {e}"
    )
