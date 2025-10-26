from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.crud.goal import goal as crud_goal
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalOut, GoalUpdate
from app.utils.responses import success_response, error_response, ResponseModel
from typing import Optional

router = APIRouter(prefix="/goals", tags=["goals"])

"""
Cria uma nova meta
"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[GoalOut])
def create_goal(goal_in: GoalCreate, db: Session = Depends(get_db)):
  goal = crud_goal.create(db, goal_in)
  return success_response(
    data=GoalOut.from_orm(goal).model_dump(),
    message="Meta criada com sucesso.",
    status_code=status.HTTP_201_CREATED
  )

"""
Atualiza os dados de uma meta
"""
@router.patch("/{goal_id}", response_model=ResponseModel[GoalOut])
def update_goal(goal_id: int, goal_in: GoalUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  obj = crud_goal.get(db, goal_id)

  # Se não encontrar, retorna erro
  if not obj:
    return error_response(
      error="Goal not found",
      message="Meta não encontrada para atualização.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  updated_goal = crud_goal.update(db, obj, goal_in)
  return success_response(
    data=GoalOut.from_orm(updated_goal).model_dump(mode="json"),
    message="Meta atualizada com sucesso."
  )

"""
Obtém os dados de uma meta especifica pelo Id
"""
@router.get("/{goal_id}", response_model=ResponseModel[GoalOut])
def read_goal(goal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  obj = crud_goal.get(db, goal_id)

  # Se não encontrar retorna erro
  if not obj:
    return error_response(
      error="Goal not found",
      message="Meta não encontrada para atualização.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  return success_response(
      data=GoalOut.from_orm(obj).model_dump(mode="json"),
      message="Meta encontrada com sucesso."
  )

# TODO: ADICIONAR OS PARAMETROS DE PESQUISA DE METAS AQUI
"""
Obtém os dados de todas as metas
"""
@router.get("/", response_model=ResponseModel[list[GoalOut]])
def read_goals(
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user),
  user_id: Optional[int] = Query(None, description="Filtro por código do usuário"),
  category_id: Optional[int] = Query(None, description="Filtro por código da categoria"),
  initial_month: Optional[int] = Query(None, description="Filtro pelo mês inicial (1-12)"),
  initial_year: Optional[int] = Query(None, description="Filtro pelo ano inicial (ex: 2023)"),
  final_month: Optional[int] = Query(None, description="Filtro pelo mês final (1-12)"),
  final_year: Optional[int] = Query(None, description="Filtro pelo ano final (ex: 2023)"),
):
  if(initial_month and not initial_year) or (final_month and not final_year):
    return error_response(
      error="Invalid date filter",
      message="Filtros de data incompletos. Por favor, forneça tanto o mês quanto o ano para os filtros de data.",
      status_code=status.HTTP_400_BAD_REQUEST
    )

  if((initial_month is not None and (initial_month < 1 or initial_month > 12)) or
     (final_month is not None and (final_month < 1 or final_month > 12))):
    return error_response(
      error="Invalid month",
      message="Os meses devem estar entre 1 e 12.",
      status_code=status.HTTP_400_BAD_REQUEST
    )

  obj = crud_goal.get_many(
    db,
    user_id=user_id,
    category_id=category_id,
    initial_month=initial_month,
    initial_year=initial_year,
    final_month=final_month,
    final_year=final_year
  )

  if not obj:
    return error_response(
      error="Goal not found",
      message="Meta não encontrada.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  data = [
    GoalOut(
        id=item.id,
        month=item.month,
        year=item.year,
        value=item.value,
        user_id=item.user_id,
        category_id=item.category_id,
        user_name=item.user.full_name if item.user else None,
        category_name=item.category.name if item.category else None
    ).model_dump(mode="json")
    for item in obj
  ]

  return success_response(
      data=data,
      message="Categorias encontradas com sucesso."
  )

"""
Remove uma categoria do sistema
"""
@router.delete("/{goal_id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[None])
def delete_user(goal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  obj = crud_goal.remove(db, goal_id)

  # Se o objeto não foi encontrado para remoção, retorna erro
  if not obj:
    return error_response(
      error="Goal not found",
      message="Meta não encontrada para exclusão.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Retorna uma mensagem de sucesso, sem dados adicionais
  return success_response(
    message="Meta removida com sucesso."
  )
