# app/api/routers/entry.py (Versão Corrigida e Segura)

from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional, List

# <-- CORREÇÃO 1: Importar a dependência com o nome correto
from app.api.deps import get_db, get_current_active_user
from app.crud.entry import entry as crud_entry
from app.models.user import User
from app.schemas.entry import EntryCreate, EntryOut, EntryUpdate
from app.utils.responses import ResponseModel, success_response, error_response

# O prefixo e a tag estão corretos!
router = APIRouter(prefix="/entries", tags=["Entries"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[EntryOut])
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
    )


@router.get("/", response_model=ResponseModel[List[EntryOut]])
def read_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # <-- CORREÇÃO: Proteger a rota
    title: Optional[str] = Query(None, description="Filtro pelo título (case-insensitive)"),
    start_date: Optional[date] = Query(None, description="Data inicial do filtro"),
    end_date: Optional[date] = Query(None, description="Data final do filtro")
):
    """
    Lista todos os lançamentos financeiros DO USUÁRIO LOGADO.
    """
    # <-- CORREÇÃO 4: Chamar uma função do CRUD que busca apenas os dados do usuário dono
    entries = crud_entry.get_many_by_owner(
        db, user_id=current_user.id, title=title, start_date=start_date, end_date=end_date
    )
    
    data = [EntryOut.from_orm(entry).model_dump(mode="json") for entry in entries]
    
    return success_response(
        data=data,
        message="Lançamentos encontrados com sucesso."
    )


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