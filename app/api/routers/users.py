# app/api/routers/users.py (Versão Corrigida e Final)

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user # A importação está correta!
from app.crud.user import user as crud_user
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.utils.responses import success_response, error_response
from app.utils.responses import ResponseModel

router = APIRouter(prefix="/users", tags=["users"])

"""
Cria um novo usuário. (Esta rota é pública, não precisa de login, por isso está correta).
"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[UserOut])
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
  if crud_user.get_by_email(db, user_in.email):
    return error_response(
      error="Email already registered",
      message="O e-mail fornecido já está em uso.",
      status_code=status.HTTP_400_BAD_REQUEST
    )
  user = crud_user.create(db, user_in)
  return success_response(
    data=UserOut.from_orm(user).model_dump(mode="json"),
    message="Usuário criado com sucesso.",
    status_code=status.HTTP_201_CREATED
  )

"""
Obtém os dados de um usuário específico pelo ID. (Precisa de login).
"""
@router.get("/{user_id}", response_model=ResponseModel[UserOut])
def read_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- CORREÇÃO AQUI
):
  obj = crud_user.get(db, user_id)
  if not obj:
    return error_response(
      error="User not found",
      message="Usuário não encontrado.",
      status_code=status.HTTP_404_NOT_FOUND
    )
  return success_response(
    data=UserOut.from_orm(obj).model_dump(mode="json"),
    message="Usuário encontrado com sucesso."
  )

"""
Atualiza os dados de um usuário. (Precisa de login).
"""
@router.patch("/{user_id}", response_model=ResponseModel[UserOut])
def update_user(
    user_id: int, 
    user_in: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- CORREÇÃO AQUI
):
  obj = crud_user.get(db, user_id)
  if not obj:
    return error_response(
      error="User not found",
      message="Usuário não encontrado para atualização.",
      status_code=status.HTTP_404_NOT_FOUND
    )
  
  # LÓGICA DE AUTORIZAÇÃO (Importante para o futuro!)
  # Garante que um usuário só possa editar a si mesmo (a menos que seja um admin)
  # if obj.id != current_user.id:
  #   return error_response(error="Forbidden", message="Você não tem permissão para editar este usuário.", status_code=403)

  updated_user = crud_user.update(db, obj, user_in)
  return success_response(
    data=UserOut.from_orm(updated_user).model_dump(mode="json"),
    message="Usuário atualizado com sucesso."
  )

"""
Remove um usuário do sistema. (Precisa de login).
"""
@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[None])
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- CORREÇÃO AQUI
):
  obj = crud_user.remove(db, user_id)
  if not obj:
    return error_response(
      error="User not found",
      message="Usuário não encontrado para exclusão.",
      status_code=status.HTTP_404_NOT_FOUND
    )
  return success_response(
    message="Usuário removido com sucesso."
  )