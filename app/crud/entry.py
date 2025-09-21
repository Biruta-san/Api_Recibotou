from sqlalchemy.orm import Session
from app.models.entry import Entry
from app.models.user import User
from app.schemas.entry import EntryCreate, EntryUpdate
from datetime import date
from typing import Optional
from sqlalchemy import func

class CRUDEntry:
  def get(self, db: Session, id: int) -> Entry | None:
    return db.get(Entry, id)

  def get_many(
    self,
    db: Session,
    title: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
  ):
    query = db.query(Entry)

    if title:
      # filtro case-insensitive
      query = query.filter(func.lower(Entry.title).like(f"%{title.lower()}%"))

    if start_date:
      query = query.filter(Entry.entry_date >= start_date)

    if end_date:
      query = query.filter(Entry.entry_date <= end_date)

    return query.all()

  def create(self, db: Session, obj_in: EntryCreate) -> Entry:
    db_obj = Entry(
      title=obj_in.title,
      entry_date=obj_in.entry_date,
      description=obj_in.description,
      value=obj_in.value,
      entry_type_id=obj_in.entry_type_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def update(self, db: Session, db_obj: Entry, obj_in: EntryUpdate) -> Entry:
    db_obj.title = obj_in.title
    db_obj.entry_date = obj_in.entry_date
    db_obj.description = obj_in.description
    db_obj.value = obj_in.value
    db_obj.entry_type_id = obj_in.entry_type_id

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def remove(self, db: Session, id: int) -> Entry | None:
    obj = self.get(db, id)
    if obj:
      db.delete(obj)
      db.commit()
    return obj

entry = CRUDEntry()
