from sqlalchemy.orm import Session
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate
from typing import Optional

class CRUDGoal:
  def get(self, db: Session, id: int) -> Goal | None:
    return db.get(Goal, id)

  def get_many(
      self,
      db: Session,
      user_id: Optional[int] = None,
      category_id: Optional[int] = None,
      initial_month: Optional[int] = None,
      initial_year: Optional[int] = None,
      final_month: Optional[int] = None,
      final_year: Optional[int] = None,
  ):
    query = db.query(Goal)

    if user_id:
      query = query.filter(Goal.user_id == user_id)
    if category_id:
      query = query.filter(Goal.category_id == category_id)
    if initial_month and initial_year:
      query = query.filter(Goal.year >= initial_year)
      query = query.filter(Goal.month >= initial_month)
    if final_month and final_year:
      query = query.filter(Goal.year <= final_year)
      query = query.filter(Goal.month <= final_month)

    return query.all()

  def create(self, db: Session, obj_in: GoalCreate) -> Goal:
    db_obj = Goal(
      month=obj_in.month,
      year=obj_in.year,
      value=obj_in.value,
      user_id=obj_in.user_id,
      category_id=obj_in.category_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def update(self, db: Session, db_obj: Goal, obj_in: GoalUpdate) -> Goal:
    db_obj.month = obj_in.month
    db_obj.year = obj_in.year
    db_obj.value = obj_in.value
    db_obj.user_id = obj_in.user_id
    db_obj.category_id = obj_in.category_id
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def remove(self, db: Session, id: int) -> Goal | None:
    obj = self.get(db, id)
    if obj:
      db.delete(obj)
      db.commit()
    return obj

category = CRUDGoal()
