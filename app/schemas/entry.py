from pydantic import BaseModel
from datetime import date

class EntryBase(BaseModel):
  title: str
  entry_date: date
  description: str | None = None
  value: float
  entry_type_id: int
  category_id: int
  user_id: int

class EntryCreate(EntryBase):
  pass

class EntryUpdate(EntryBase):
  pass

class EntryOut(EntryBase):
  id: int
  entry_type_name: str | None
  category_name: str | None
  user_name: str | None

  class Config:
    from_attributes = True

  @classmethod
  def from_orm(cls, obj):
    return cls.model_validate({
      "id": obj.id,
      "title": obj.title,
      "entry_date": obj.entry_date,
      "description": obj.description,
      "value": obj.value,
      "entry_type_id": obj.entry_type_id,
      "entry_type_name": obj.entry_type.name if obj.entry_type else None,
      "category_name": obj.category.name if obj.category else None,
      "user_name": obj.user.full_name if obj.user else None,
    })
