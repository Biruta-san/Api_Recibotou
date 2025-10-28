from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional, List

# CORREÇÃO 1: Padronizar o import de segurança
from app.api.deps import get_db, get_current_active_user 
from app.crud.entry import entry as crud_entry
from app.crud.goal import goal as crud_goal
from app.crud.notification import notification as crud_notification
from app.models.user import User
from app.schemas.entry import EntryCreate, EntryOut, EntryUpdate
from app.schemas.notification import NotificationCreate # Necessário para a lógica de Metas
from app.utils.responses import ResponseModel, success_response, error_response


router = APIRouter(prefix="/entries", tags=["Entries"])


"""
Cria um novo lançamento financeiro para o usuário logado (Integrando Metas e Segurança).
"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[EntryOut])
def create_entry(
    entry_in: EntryCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- SEGURANÇA APLICADA
):
    """Cria um novo lançamento financeiro para o usuário logado."""
    
    # CRIAÇÃO DO LANÇAMENTO COM DONO
    entry = crud_entry.create_with_owner(db=db, obj_in=entry_in, user_id=current_user.id)
    
    if not entry:
        return error_response(
            error="Entry creation failed",
            message="Falha ao criar o lançamento.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # LÓGICA DE METAS E NOTIFICAÇÕES (Do código do seu colega, agora ativa)
    general_goal = crud_goal.get_goal_by_data(
        db,
        month=entry.entry_date.month,
        year=entry.entry_date.year,
        user_id=current_user.id # Usando o ID do usuário logado
    )

    category_goal = None
    if entry_in.category_id:
        category_goal = crud_goal.get_goal_by_data(
            db,
            month=entry.entry_date.month,
            year=entry.entry_date.year,
            user_id=current_user.id, # Usando o ID do usuário logado
            category_id=entry_in.category_id
        )

    # Verifica se a Meta Geral foi atingida
    if general_goal:
        total_entries_value = crud_entry.get_sum_by_period(
            db,
            month=entry.entry_date.month,
            year=entry.entry_date.year,
            user_id=current_user.id
        )
        if total_entries_value > general_goal.value:
            crud_notification.create(
                db,
                NotificationCreate(
                    title="Meta Geral Atingida",
                    message=f"Você atingiu sua meta geral de {general_goal.value:.2f} com um total de entradas de {total_entries_value:.2f}.",
                    user_id=current_user.id
                )
            )

    # Verifica se a Meta por Categoria foi atingida
    if category_goal:
        total_category_entries_value = crud_entry.get_sum_by_period(
            db,
            month=entry.entry_date.month,
            year=entry.entry_date.year,
            user_id=current_user.id,
            category_id=entry_in.category_id
        )
        if total_category_entries_value > category_goal.value:
            crud_notification.create(
                db,
                NotificationCreate(
                    title="Meta por Categoria Atingida",
                    message=f"Você atingiu sua meta de {category_goal.value:.2f} para a categoria com um total de entradas de {total_category_entries_value:.2f}.",
                    user_id=current_user.id
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
def update_entry(
    entry_id: int, 
    entry_in: EntryUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- SEGURANÇA APLICADA
):
    """Atualiza os dados de um lançamento."""
    obj = crud_entry.get(db, entry_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lançamento não encontrado.")

    # GARANTIA DE SEGURANÇA: Só o dono pode atualizar
    if obj.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não tem permissão para editar este recurso.")

    updated_entry = crud_entry.update(db, db_obj=obj, obj_in=entry_in)

    if not updated_entry:
        return error_response(
            error="Error updating entry",
            message="Falha ao atualizar o lançamento.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # LÓGICA DE METAS PÓS-ATUALIZAÇÃO (Completa)
    # Requer os mesmos CRUDS e schemas para Goal e Notification
    # ... (A lógica de metas do seu colega é longa, mas foi mesclada aqui) ...
    general_goal = crud_goal.get_goal_by_data(
        db,
        month=updated_entry.entry_date.month,
        year=updated_entry.entry_date.year,
        user_id=current_user.id
    )
    category_goal = None
    if entry_in.category_id:
        category_goal = crud_goal.get_goal_by_data(
            db,
            month=updated_entry.entry_date.month,
            year=updated_entry.entry_date.year,
            user_id=current_user.id,
            category_id=entry_in.category_id
        )

    # Verifica se a Meta Geral foi atingida após a atualização
    if general_goal:
        total_entries_value = crud_entry.get_sum_by_period(
            db,
            month=updated_entry.entry_date.month,
            year=updated_entry.entry_date.year,
            user_id=current_user.id
        )
        if total_entries_value > general_goal.value:
            crud_notification.create(
                db,
                NotificationCreate(
                    title="Meta Geral Atingida",
                    message=f"Você atingiu sua meta geral de {general_goal.value:.2f} com um total de entradas de {total_entries_value:.2f}.",
                    user_id=current_user.id
                )
            )
    
    # Verifica se a Meta por Categoria foi atingida após a atualização
    if category_goal:
        total_category_entries_value = crud_entry.get_sum_by_period(
            db,
            month=updated_entry.entry_date.month,
            year=updated_entry.entry_date.year,
            user_id=current_user.id,
            category_id=entry_in.category_id
        )
        if total_category_entries_value > category_goal.value:
            crud_notification.create(
                db,
                NotificationCreate(
                    title="Meta por Categoria Atingida",
                    message=f"Você atingiu sua meta de {category_goal.value:.2f} para a categoria com um total de entradas de {total_category_entries_value:.2f}.",
                    user_id=current_user.id
                )
            )

    return success_response(
        data=EntryOut.from_orm(updated_entry).model_dump(mode="json"),
        message="Lançamento atualizado com sucesso."
    )


"""
Obtém os dados de um lançamento específico pelo ID.
"""
@router.get("/{entry_id}", response_model=ResponseModel[EntryOut])
def read_entry(
    entry_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- SEGURANÇA APLICADA
):
    """Obtém os dados de um lançamento específico."""
    obj = crud_entry.get(db, entry_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lançamento não encontrado.")

    # GARANTIA DE SEGURANÇA: Só o dono pode ver
    if obj.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não tem permissão para acessar este recurso.")

    return success_response(
        data=EntryOut.from_orm(obj).model_dump(mode="json"),
        message="Lançamento encontrado com sucesso."
    )


"""
Obtém os dados de todos os lançamentos do usuário logado (com filtros).
"""
@router.get("/", response_model=ResponseModel[List[EntryOut]])
def read_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # <-- SEGURANÇA APLICADA
    title: Optional[str] = Query(None, description="Filtro pelo título (case-insensitive)"),
    start_date: Optional[date] = Query(None, description="Data inicial do filtro"),
    end_date: Optional[date] = Query(None, description="Data final do filtro"),
    category_id: Optional[int] = Query(None, description="Filtro pelo ID da categoria"),
    entry_type_id: Optional[int] = Query(None, description="Filtro pelo ID do tipo de lançamento"),
):
    # CORREÇÃO CRUCIAL: Usar get_many_by_owner e injetar o ID do usuário
    obj = crud_entry.get_many_by_owner(
        db,
        user_id=current_user.id,
        title=title,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id,
        entry_type_id=entry_type_id
    )

    if not obj:
        return error_response(
            error="Entries not found",
            message="Lançamentos não encontrados.",
            status_code=status.HTTP_404_NOT_FOUND
        )

    # Usando o from_orm e model_dump para serializar corretamente
    data = [EntryOut.from_orm(item).model_dump(mode="json") for item in obj]

    return success_response(
        data=data,
        message="Lançamentos encontrados com sucesso."
    )


"""
Remove um lançamento do sistema.
"""
@router.delete("/{entry_id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[None])
def delete_entry(
    entry_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- SEGURANÇA APLICADA
):
    # Lógica de segurança para garantir que o usuário é o dono antes de remover
    entry_to_delete = crud_entry.get(db, entry_id)
    if not entry_to_delete:
        return error_response(
            error="Entry not found",
            message="Lançamento não encontrado para exclusão.",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    if entry_to_delete.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não tem permissão para excluir este recurso.")

    # Tenta remover o lançamento
    obj = crud_entry.remove(db, entry_id)

    # Retorna uma mensagem de sucesso
    return success_response(
        message="Lançamento removido com sucesso."
    )