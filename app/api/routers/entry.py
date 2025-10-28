<<<<<<< HEAD
# app/api/routers/entry.py (Versão Corrigida e Segura)

from fastapi import APIRouter, Depends, status, Query, HTTPException
=======
from fastapi import APIRouter, Depends, status, Query
from app.utils.responses import success_response, error_response, ResponseModel
from app.schemas.entry import EntryOut, EntryCreate, EntryUpdate
from app.schemas.notification import NotificationCreate
from app.api.deps import get_db, get_current_user
>>>>>>> origin/main
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from app.api.deps import get_db, get_current_user
from app.crud.entry import entry as crud_entry
from app.crud.goal import goal as crud_goal
from app.crud.notification import notification as crud_notification
from app.models.user import User
from app.schemas.entry import EntryCreate, EntryOut, EntryUpdate
from app.utils.responses import ResponseModel, success_response, error_response

# O prefixo e a tag estão corretos!
router = APIRouter(prefix="/entries", tags=["Entries"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[EntryOut])
<<<<<<< HEAD
<<<<<<< HEAD
def create_entry(
    entry_in: EntryCreate, 
    db: Session = Depends(get_db), 
    # <-- CORREÇÃO 2: Proteger a rota e obter o usuário logado
    current_user: User = Depends(get_current_active_user)
):
    """
    Cria um novo lançamento financeiro para o usuário logado.
    """
    # <-- CORREÇÃO 3: Usar a função do CRUD que associa o usuário ao lançamento
    entry = crud_entry.create_with_owner(db=db, obj_in=entry_in, user_id=current_user.id)
    
    return success_response(
        data=EntryOut.from_orm(entry).model_dump(mode="json"),
        message="Lançamento criado com sucesso.",
        status_code=status.HTTP_201_CREATED
=======
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
>>>>>>> 7dc122e3ab86853868dc347cecc7855854553682
    )

  # Atualiza o lançamento e retorna os novos dados
  updated_entry = crud_entry.update(db, obj, entry_in)
  return success_response(
    data=EntryOut.from_orm(updated_entry).model_dump(mode="json"),
    message="Lançamento atualizado com sucesso."
  )

<<<<<<< HEAD
@router.get("/", response_model=ResponseModel[List[EntryOut]])
def read_entries(
=======
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
>>>>>>> 7dc122e3ab86853868dc347cecc7855854553682
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

<<<<<<< HEAD
=======
def create_entry(entry_in: EntryCreate, db: Session = Depends(get_db)):
  # Cria o Lançamento no banco de dados e retorna
  entry = crud_entry.create(db, entry_in)

  if not entry:
    return error_response(
      error="Entry creation failed",
      message="Falha ao criar o lançamento.",
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

  general_goal = crud_goal.get_goal_by_data(
    db,
    month=entry.entry_date.month,
    year=entry.entry_date.year,
    user_id=entry_in.user_id
  )

  category_goal = None

  if(entry_in.category_id):
    category_goal = crud_goal.get_goal_by_data(
      db,
      month=entry.entry_date.month,
      year=entry.entry_date.year,
      user_id=entry_in.user_id,
      category_id=entry_in.category_id
    )

  if general_goal:
    total_entries_value = crud_entry.get_sum_by_period(
      db,
      month=entry.entry_date.month,
      year=entry.entry_date.year,
      user_id=entry_in.user_id
    )

    if total_entries_value > general_goal.value:
      crud_notification.create(
        db,
        NotificationCreate(
          title="Meta Geral Atingida",
          message=f"Você atingiu sua meta geral de {general_goal.value:.2f} com um total de entradas de {total_entries_value:.2f}.",
          user_id=entry_in.user_id
        )
      )

  if category_goal:
    total_category_entries_value = crud_entry.get_sum_by_period(
      db,
      month=entry.entry_date.month,
      year=entry.entry_date.year,
      user_id=entry_in.user_id,
      category_id=entry_in.category_id
    )

    if total_category_entries_value > category_goal.value:
      crud_notification.create(
        db,
        NotificationCreate(
          title="Meta por Categoria Atingida",
          message=f"Você atingiu sua meta de {category_goal.value:.2f} para a categoria com um total de entradas de {total_category_entries_value:.2f}.",
          user_id=entry_in.user_id
        )
      )

  return success_response(
    data=EntryOut.from_orm(entry).model_dump(mode="json"),
    message="Lançamento criado com sucesso.",
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

  if not updated_entry:
    return error_response(
      error="Error updating entry",
      message="Falha ao atualizar o lançamento.",
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

  general_goal = crud_goal.get_goal_by_data(
    db,
    month=updated_entry.entry_date.month,
    year=updated_entry.entry_date.year,
    user_id=entry_in.user_id
  )

  category_goal = None

  if(entry_in.category_id):
    category_goal = crud_goal.get_goal_by_data(
      db,
      month=updated_entry.entry_date.month,
      year=updated_entry.entry_date.year,
      user_id=entry_in.user_id,
      category_id=entry_in.category_id
    )

  if general_goal:
    total_entries_value = crud_entry.get_sum_by_period(
      db,
      month=updated_entry.entry_date.month,
      year=updated_entry.entry_date.year,
      user_id=entry_in.user_id
    )

    if total_entries_value > general_goal.value:
      crud_notification.create(
        db,
        NotificationCreate(
          title="Meta Geral Atingida",
          message=f"Você atingiu sua meta geral de {general_goal.value:.2f} com um total de entradas de {total_entries_value:.2f}.",
          user_id=entry_in.user_id
        )
      )

  if category_goal:
    total_category_entries_value = crud_entry.get_sum_by_period(
      db,
      month=updated_entry.entry_date.month,
      year=updated_entry.entry_date.year,
      user_id=entry_in.user_id,
      category_id=entry_in.category_id
    )

    if total_category_entries_value > category_goal.value:
      crud_notification.create(
        db,
        NotificationCreate(
          title="Meta por Categoria Atingida",
          message=f"Você atingiu sua meta de {category_goal.value:.2f} para a categoria com um total de entradas de {total_category_entries_value:.2f}.",
          user_id=entry_in.user_id
        )
      )

  return success_response(
    data=EntryOut.from_orm(updated_entry).model_dump(mode="json"),
    message="Lançamento atualizado com sucesso."
  )

"""
Obtém os dados de um tipo de lançamento específico pelo ID.
"""
>>>>>>> origin/main
@router.get("/{entry_id}", response_model=ResponseModel[EntryOut])
def read_entry(
    entry_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- CORREÇÃO: Proteger a rota
):
    """
    Obtém os dados de um lançamento específico.
    """
    obj = crud_entry.get(db, entry_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado.")

    # <-- CORREÇÃO 5: Garantir que o usuário só possa ver seus próprios lançamentos
    if obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não tem permissão para acessar este recurso.")

    return success_response(
        data=EntryOut.from_orm(obj).model_dump(mode="json"),
        message="Lançamento encontrado com sucesso."
    )

<<<<<<< HEAD

@router.patch("/{entry_id}", response_model=ResponseModel[EntryOut])
def update_entry(
    entry_id: int, 
    entry_in: EntryUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- CORREÇÃO: Proteger a rota
):
    """
    Atualiza os dados de um lançamento.
    """
    obj = crud_entry.get(db, entry_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado.")

    # <-- CORREÇÃO 6: Garantir que o usuário só possa editar seus próprios lançamentos
    if obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não tem permissão para editar este recurso.")

    updated_entry = crud_entry.update(db, db_obj=obj, obj_in=entry_in)
    return success_response(
        data=EntryOut.from_orm(updated_entry).model_dump(mode="json"),
        message="Lançamento atualizado com sucesso."
    )
=======
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
    end_date: Optional[date] = Query(None, description="Data final do filtro"),
    user_id: Optional[int] = Query(None, description="Filtro pelo ID do usuário"),
    category_id: Optional[int] = Query(None, description="Filtro pelo ID da categoria"),
    entry_type_id: Optional[int] = Query(None, description="Filtro pelo ID do tipo de lançamento"),
  ):
  # Busca o tipo de lançamento no banco de dados
  obj = crud_entry.get_many(
    db,
    title=title,
    start_date=start_date,
    end_date=end_date,
    user_id=user_id,
    category_id=category_id,
    entry_type_id=entry_type_id
)

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
        entry_type_name=item.entry_type.name if item.entry_type else None,
        category_id=item.category_id,
        category_name=item.category.name if item.category else None,
        user_id=item.user_id,
        user_name=item.user.full_name if item.user else None,
    ).model_dump(mode="json")  # garante que date seja serializável
    for item in obj
  ]

=======
>>>>>>> 7dc122e3ab86853868dc347cecc7855854553682
  # Retorna os dados do tipo de lançamento em uma resposta de sucesso
  return success_response(
      data=data,
      message="Lançamentos encontrados com sucesso."
  )

<<<<<<< HEAD
"""
Remove um lançamento do sistema.
"""
@router.delete("/{entry_id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[None])
def delete_entry(entry_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # Tenta remover o lançamento
  obj = crud_entry.remove(db, entry_id)


  # Se o objeto não foi encontrado para remoção, retorna erro
  if not obj:
    return error_response(
      error="Entry not found",
      message="Lançamento não encontrado para exclusão.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Retorna uma mensagem de sucesso, sem dados adicionais
  return success_response(
    message="Lançamento removido com sucesso."
  )
>>>>>>> origin/main
=======
>>>>>>> 7dc122e3ab86853868dc347cecc7855854553682
