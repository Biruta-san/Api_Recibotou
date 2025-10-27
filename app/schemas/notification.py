from datetime import datetime
from pydantic import BaseModel

class NotificationBase(BaseModel):
  title: str
  message: str | None = None
  user_id: int
  read: bool = False

class NotificationCreate(NotificationBase):
  pass

class NotificationUpdate(NotificationBase):
  pass

class NotificationOut(NotificationBase):
  id: int
  user_name: str | None
  created_at: datetime | None = None

  class Config:
    from_attributes = True

  @classmethod
  def from_orm(cls, obj):
    return cls.model_validate({
      "id": obj.id,
      "title": obj.title,
      "message": obj.message,
      "user_id": obj.user_id,
      "user_name": obj.user.full_name if obj.user else None,
      "read": obj.read,
      "created_at": obj.created_at
    })
