from fastapi import APIRouter, Depends, status, Query
from app.utils.responses import success_response, error_response, ResponseModel
from app.schemas.notification import NotificationOut, NotificationCreate, NotificationUpdate
from app.api.deps import get_db, get_current_user
from sqlalchemy.orm import Session
from app.crud.notification import notification as crud_notification
from app.models.user import User
from datetime import date
from typing import Optional

router = APIRouter(prefix="/notifications", tags=["notifications"])

"""
Cria um novo notificação.
"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[NotificationOut])
def create_notification(notification_in: NotificationCreate, db: Session = Depends(get_db)):
  notification_type = crud_notification.create(db, notification_in)
  return success_response(
    data=NotificationOut.from_orm(notification_type).model_dump(mode="json"),
    message="Notificação criada com sucesso.",
    status_code=status.HTTP_201_CREATED
  )

"""
Atualiza os dados de uma notificação.
"""
@router.patch("/{notification_id}", response_model=ResponseModel[NotificationOut])
def update_notification(notification_id: int, notification_in: NotificationUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # Busca a notificação a ser atualizada
  obj = crud_notification.get(db, notification_id)

  # Se não encontrar, retorna erro
  if not obj:
    return error_response(
      error="Notification not found",
      message="Notificação não encontrada para atualização.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Atualiza a notificação e retorna os novos dados
  updated_notification = crud_notification.update(db, obj, notification_in)
  return success_response(
    data=NotificationOut.from_orm(updated_notification).model_dump(mode="json"),
    message="Notificação atualizada com sucesso."
  )

"""
Marca uma notificação como lida.
"""
@router.patch("/{notification_id}/read", response_model=ResponseModel[NotificationOut])
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # Busca a notificação a ser atualizada
  obj = crud_notification.mark_as_read(db, notification_id)

  # Se não encontrar, retorna erro
  if not obj:
    return error_response(
      error="Notification not found",
      message="Notificação não encontrada para atualização.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Atualiza a notificação e retorna os novos dados
  updated_notification = crud_notification.update(db, obj, notification_in)
  return success_response(
    data=NotificationOut.from_orm(updated_notification).model_dump(mode="json"),
    message="Notificação atualizada com sucesso."
  )

"""
Obtém os dados de uma notificação específica pelo ID.
"""
@router.get("/{notification_id}", response_model=ResponseModel[NotificationOut])
def read_notification(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  # Busca a notificação no banco de dados
  obj = crud_notification.get(db, notification_id)

  # Se a notificação não for encontrada, retorna um erro padronizado
  if not obj:
    return error_response(
      error="Notification not found",
      message="Notificação não encontrada.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  # Retorna os dados da notificação em uma resposta de sucesso
  return success_response(
      data=NotificationOut.from_orm(obj).model_dump(mode="json"),
      message="Notificação encontrada com sucesso."
  )

"""
Obtém os dados da lista de notificações com filtros opcionais.
"""
@router.get("/", response_model=ResponseModel[list[NotificationOut]])
def read_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    title: Optional[str] = Query(None, description="Filtro pelo título (case-insensitive)"),
    start_date: Optional[date] = Query(None, description="Data inicial do filtro"),
    end_date: Optional[date] = Query(None, description="Data final do filtro"),
    user_id: Optional[int] = Query(None, description="Filtro pelo ID do usuário"),
    read: Optional[bool] = Query(None, description="Filtro pelo status de leitura"),
  ):
  # Busca o tipo de notificação no banco de dados
  if not user_id:
    user_id = current_user.id

  obj = crud_notification.get_many(db, title=title, start_date=start_date, end_date=end_date, user_id=user_id, read=read)

  # Se o tipo de notificação não for encontrado, retorna um erro padronizado
  if not obj:
    return error_response(
      error="Notifications not found",
      message="Notificações não encontradas.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  data = [
    NotificationOut(
        id=item.id,
        title=item.title,
        message=item.message,
        read=item.read,
        created_at=item.created_at,
        user_id=item.user_id,
        user_name=item.user.full_name if item.user else None
    ).model_dump(mode="json")  # garante que date seja serializável
    for item in obj
  ]

  # Retorna os dados do tipo de notificação em uma resposta de sucesso
  return success_response(
      data=data,
      message="Notificações encontradas com sucesso."
  )

