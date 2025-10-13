from fastapi import APIRouter, Depends, status, Query
from app.utils.responses import success_response, error_response, ResponseModel
from app.schemas.entry import EntryOut, EntryCreate, EntryUpdate
from app.api.deps import get_db, get_current_user
from sqlalchemy.orm import Session
from app.crud.entry import entry as crud_entry
from app.models.user import User
from datetime import date
from typing import Optional

router = APIRouter(prefix="/entries", tags=["entries"])

"""
Cria um novo lançamento financeiro.
"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[EntryOut])
def create_entry(entry_in: EntryCreate, db: Session = Depends(get_db)):
  # Cria o Tipo de lançamento no banco de dados e retorna
  entry_type = crud_entry.create(db, entry_in)
  return success_response(
    data=EntryOut.from_orm(entry_type).model_dump(mode="json"),
    message="Tipo de lançamento criado com sucesso.",
    status_code=status.HTTP_201_CREATED
  )

"""
Atualiza os dados de um lançamento.
"""
@router.patch("/{entry_id}", response_model=ResponseModel[EntryOut])
def update_entry_type(entry_id: int, entry_in: EntryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # Busca o lançamento a ser atualizado
  obj = crud_entry.get(db, entry_id)

  # Se não encontrar, retorna erro
  if not obj:
    return error_response(
      error="Entry not found",
      message="Lançamento não encontrado para atualização.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Atualiza o lançamento e retorna os novos dados
  updated_entry = crud_entry.update(db, obj, entry_in)
  return success_response(
    data=EntryOut.from_orm(updated_entry).model_dump(mode="json"),
    message="Lançamento atualizado com sucesso."
  )

"""
Obtém os dados de um tipo de lançamento específico pelo ID.
"""
@router.get("/{entry_id}", response_model=ResponseModel[EntryOut])
def read_entry_type(entry_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # Busca o tipo de lançamento no banco de dados
  obj = crud_entry.get(db, entry_id)

  # Se o tipo de lançamento não for encontrado, retorna um erro padronizado
  if not obj:
    return error_response(
      error="Entry not found",
      message="Lançamento não encontrado.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Retorna os dados do tipo de lançamento em uma resposta de sucesso
  return success_response(
      data=EntryOut.from_orm(obj).model_dump(mode="json"),
      message="Lançamento encontrado com sucesso."
  )

"""
Obtém os dados de todos os tipos de lançamento.
"""
@router.get("/", response_model=ResponseModel[list[EntryOut]])
def read_entry_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    title: Optional[str] = Query(None, description="Filtro pelo título (case-insensitive)"),
    start_date: Optional[date] = Query(None, description="Data inicial do filtro"),
    end_date: Optional[date] = Query(None, description="Data final do filtro")
  ):
  # Busca o tipo de lançamento no banco de dados
  obj = crud_entry.get_many(db, title=title, start_date=start_date, end_date=end_date)

  # Se o tipo de lançamento não for encontrado, retorna um erro padronizado
  if not obj:
    return error_response(
      error="Entries not found",
      message="Lançamentos não encontrados.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  data = [
    EntryOut(
        id=item.id,
        title=item.title,
        entry_date=item.entry_date,
        description=item.description,
        value=item.value,
        entry_type_id=item.entry_type_id,
        entry_type_name=item.entry_type.name if item.entry_type else None
    ).model_dump(mode="json")  # garante que date seja serializável
    for item in obj
  ]

  # Retorna os dados do tipo de lançamento em uma resposta de sucesso
  return success_response(
      data=data,
      message="Lançamentos encontrados com sucesso."
  )

