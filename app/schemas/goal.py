from pydantic import BaseModel, computed_field

class GoalBase(BaseModel):
  month: int
  year: int
  value: float
  user_id: int
  category_id: int | None = None

class GoalCreate(GoalBase):
  pass

class GoalUpdate(GoalBase):
  pass

class GoalOut(GoalBase):
  id: int
  user_name: str | None = None
  category_name: str | None = None

  @computed_field
  def mes_ano(self) -> str:
    return f"{self.month}/{self.year}"

  @classmethod
  def from_orm(cls, obj):
    return cls.model_validate({
      "id": obj.id,
      "month": obj.month,
      "year": obj.year,
      "value": obj.value,
      "user_id": obj.user_id,
      "category_id": obj.category_id,
      "user_name": obj.user.name if obj.user else None,
      "category_name": obj.category.name if obj.category else None
    })

  class Config:
    from_attributes = True
