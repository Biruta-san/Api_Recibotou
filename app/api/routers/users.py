from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.responses import StreamingResponse
from io import BytesIO
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.crud.user import user as crud_user
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.utils.responses import success_response, error_response
from app.utils.responses import ResponseModel
# Importe suas funções de resposta e o modelo

router = APIRouter(prefix="/users", tags=["users"])

"""
Cria um novo usuário.
"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[UserOut])
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
  # Verifica se o e-mail já existe no banco de dados
  if crud_user.get_by_email(db, user_in.email):
    # Retorna uma resposta de erro padronizada
    return error_response(
      error="Email already registered",
      message="O e-mail fornecido já está em uso.",
      status_code=status.HTTP_400_BAD_REQUEST
    )

  if user_in.phone_number and crud_user.get_by_phone(db, user_in.phone_number):
    # Retorna uma resposta de erro padronizada
    return error_response(
      error="Phone already registered",
      message="O telefone fornecido já está em uso.",
      status_code=status.HTTP_400_BAD_REQUEST
    )

  # Cria o usuário e o retorna em uma resposta de sucesso
  user = crud_user.create(db, user_in)
  return success_response(
    data=UserOut.from_orm(user).model_dump(mode="json"),
    message="Usuário criado com sucesso.",
    status_code=status.HTTP_201_CREATED
  )


"""
Obtém os dados de um usuário específico pelo ID.
"""
@router.get("/{user_id}", response_model=ResponseModel[UserOut])
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # Busca o usuário no banco de dados
  obj = crud_user.get(db, user_id)

  # Se o usuário não for encontrado, retorna um erro padronizado
  if not obj:
    return error_response(
      error="User not found",
      message="Usuário não encontrado.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Retorna os dados do usuário em uma resposta de sucesso
  return success_response(
    data=UserOut.from_orm(obj).model_dump(mode="json"),
    message="Usuário encontrado com sucesso."
  )


"""
Atualiza os dados de um usuário.
"""
@router.patch("/{user_id}", response_model=ResponseModel[UserOut])
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # Busca o usuário a ser atualizado
  obj = crud_user.get(db, user_id)

  # Se não encontrar, retorna erro
  if not obj:
    return error_response(
      error="User not found",
      message="Usuário não encontrado para atualização.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Atualiza o usuário e retorna os novos dados
  updated_user = crud_user.update(db, obj, user_in)
  return success_response(
    data=UserOut.from_orm(updated_user).model_dump(mode="json"),
    message="Usuário atualizado com sucesso."
  )

"""
Remove um usuário do sistema.
"""
@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[None])
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # Tenta remover o usuário
  obj = crud_user.remove(db, user_id)

  # Se o objeto não foi encontrado para remoção, retorna erro
  if not obj:
    return error_response(
      error="User not found",
      message="Usuário não encontrado para exclusão.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Retorna uma mensagem de sucesso, sem dados adicionais
  return success_response(
    message="Usuário removido com sucesso."
  )

@router.patch("/{user_id}/profile_image", response_model=ResponseModel[UserOut])
async def upload_profile_image(
    user_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
  obj = crud_user.get(db, user_id)

  # Se não encontrar, retorna erro
  if not obj:
    return error_response(
      error="User not found",
      message="Usuário não encontrado para atualização.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  profile_image = await image.read()
  updated_user = crud_user.update_profile_image(db, obj, profile_image, image.filename, image.content_type)

  return success_response(
    data=UserOut.from_orm(updated_user).model_dump(mode="json"),
    message="Usuário atualizado com sucesso."
  )


@router.get("/{user_id}/profile_image", response_model=ResponseModel[UserOut])
async def get_profile_image(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    download: bool = True
):
  user = crud_user.get(db, user_id)
  if not user:
      return error_response(
          error="User not found",
          message="Usuário não encontrado.",
          status_code=status.HTTP_404_NOT_FOUND
      )

  disposition = "attachment" if download else "inline"

  if not user.profile_image:
      return error_response(
          error="Profile image not found",
          message="Imagem de perfil não encontrada.",
          status_code=status.HTTP_404_NOT_FOUND
      )

  return StreamingResponse(
    BytesIO(user.profile_image),
    media_type=user.profile_image_type,
    headers={"Content-Disposition": f"{disposition}; filename={user.profile_image_name}"}
)
