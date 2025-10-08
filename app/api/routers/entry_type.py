from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.crud.entry_type import entry_type as crud_entry_type
from app.models.user import User
from app.schemas.entry_type import EntryTypeCreate, EntryTypeOut, EntryTypeUpdate
from app.utils.responses import success_response, error_response, ResponseModel
from app.utils.enum import TipoLancamento

router = APIRouter(prefix="/entry_types", tags=["entry_types"])

"""
Cria um novo tipo de lançamento financeiro.
"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[EntryTypeOut])
def create_entry_type(entry_type_in: EntryTypeCreate, db: Session = Depends(get_db)):
  # Cria o Tipo de lançamento no banco de dados e retorna
  entry_type = crud_entry_type.create(db, entry_type_in)
  return success_response(
    data=EntryTypeOut.from_orm(entry_type).model_dump(),
    message="Tipo de lançamento criado com sucesso.",
    status_code=status.HTTP_201_CREATED
  )

"""
Atualiza os dados de um tipo de lançamento.
"""
@router.patch("/{entry_type_id}", response_model=ResponseModel[EntryTypeOut])
def update_entry_type(entry_type_id: int, entry_type_in: EntryTypeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
  # Busca o lançamento a ser atualizado
  obj = crud_entry_type.get(db, entry_type_id)

  # Se não encontrar, retorna erro
  if not obj:
    return error_response(
      error="Entry type not found",
      message="Tipo de lançamento não encontrado para atualização.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Atualiza o tipo de lançamento e retorna os novos dados
  updated_entry_type = crud_entry_type.update(db, obj, entry_type_in)
  return success_response(
    data=EntryTypeOut.from_orm(updated_entry_type).model_dump(),
    message="Tipo de lançamento atualizado com sucesso."
  )

"""
Obtém os dados de um tipo de lançamento específico pelo ID.
"""
@router.get("/{entry_type_id}", response_model=ResponseModel[EntryTypeOut])
def read_entry_type(entry_type_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
  # Busca o tipo de lançamento no banco de dados
  obj = crud_entry_type.get(db, entry_type_id)

  # Se o tipo de lançamento não for encontrado, retorna um erro padronizado
  if not obj:
    return error_response(
      error="Entry type not found",
      message="Tipo de lançamento não encontrado.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Retorna os dados do tipo de lançamento em uma resposta de sucesso
  return success_response(
      data=EntryTypeOut.from_orm(obj).model_dump(),
      message="Tipo de lançamento encontrado com sucesso."
  )

"""
Obtém os dados de todos os tipos de lançamento.
"""
@router.get("/", response_model=ResponseModel[list[EntryTypeOut]])
def read_entry_types(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
  # Busca o tipo de lançamento no banco de dados
  obj = crud_entry_type.get_many(db)

  # Se o tipo de lançamento não for encontrado, retorna um erro padronizado
  if not obj:
    return error_response(
      error="Entry types not found",
      message="Tipos de lançamento não encontrados.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Retorna os dados do tipo de lançamento em uma resposta de sucesso
  return success_response(
      data=[EntryTypeOut.model_validate(item) for item in obj],
      message="Tipos de lançamento encontrados com sucesso."
  )

"""
Remove um usuário do sistema.
"""
@router.delete("/{entry_type_id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[None])
def delete_user(entry_type_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
  # Tenta remover o usuário
  obj = crud_entry_type.remove(db, entry_type_id)

  if entry_type_id in [TipoLancamento.DESPESA, TipoLancamento.RECEITA]:
    return error_response(
      error="Entry Type protected",
      message="Tipo de lançamento protegido e não pode ser excluído.",
      status_code=status.HTTP_403_FORBIDDEN
    )

  # Se o objeto não foi encontrado para remoção, retorna erro
  if not obj:
    return error_response(
      error="Entry Type not found",
      message="Tipo de lançamento não encontrado para exclusão.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Retorna uma mensagem de sucesso, sem dados adicionais
  return success_response(
    message="Tipo de Lançamento removido com sucesso."
  )
