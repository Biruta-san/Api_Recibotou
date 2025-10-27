from app.models.notification import Notification
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, datetime
from sqlalchemy import func
from app.schemas.notification import NotificationCreate, NotificationUpdate


class CRUDNotification:
  def get(self, db: Session, id: int) -> Notification | None:
    return db.get(Notification, id)

  def get_many(
    self,
    db: Session,
    title: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    user_id: Optional[int] = None,
    read: Optional[bool] = None,
  ):
    query = db.query(Notification)

    if title:
      query = query.filter(func.lower(Notification.title).like(f"%{title.lower()}%"))

    if start_date:
      query = query.filter(Notification.created_at >= start_date)

    if end_date:
      query = query.filter(Notification.created_at <= end_date)

    if user_id:
      query = query.filter(Notification.user_id == user_id)

    if read is not None:
      query = query.filter(Notification.read == read)

    return query.all()

  def create(self, db: Session, obj_in: NotificationCreate) -> Notification:
    db_obj = Notification(
      title=obj_in.title,
      message=obj_in.message,
      user_id=obj_in.user_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def update(self, db: Session, db_obj: Notification, obj_in: NotificationUpdate) -> Notification:
    db_obj.title = obj_in.title
    db_obj.message = obj_in.message
    db_obj.read = obj_in.read
    db_obj.user_id = obj_in.user_id

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def remove(self, db: Session, id: int) -> Notification | None:
    obj = self.get(db, id)
    if obj:
      db.delete(obj)
      db.commit()
    return obj

  def mark_as_read(self, db: Session, id: int) -> Notification | None:
    obj = self.get(db, id)
    if obj and not obj.read:
      obj.read = True
      db.add(obj)
      db.commit()
      db.refresh(obj)
    return obj

notification = CRUDNotification()
