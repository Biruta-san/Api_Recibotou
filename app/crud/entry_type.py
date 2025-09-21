from sqlalchemy.orm import Session
from app.models.entry_type import EntryType
from app.schemas.entry_type import EntryTypeCreate, EntryTypeUpdate

class CRUDEntryType:
  def get(self, db: Session, id: int) -> EntryType | None:
    return db.get(EntryType, id)

  def get_many(self, db: Session):
    return db.query(EntryType).all()

  def create(self, db: Session, obj_in: EntryTypeCreate) -> EntryType:
    db_obj = EntryType(
      name=obj_in.name,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def update(self, db: Session, db_obj: EntryType, obj_in: EntryTypeUpdate) -> EntryType:
    db_obj.name = obj_in.name
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


  def remove(self, db: Session, id: int) -> EntryType | None:
    obj = self.get(db, id)
    if obj:
      db.delete(obj)
      db.commit()
    return obj


entry_type = CRUDEntryType()