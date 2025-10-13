from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

class CRUDCategory:
  def get(self, db: Session, id: int) -> Category | None:
    return db.get(Category, id)

  def get_many(self, db: Session):
    return db.query(Category).all()

  def create(self, db: Session, obj_in: CategoryCreate) -> Category:
    db_obj = Category(
        name=obj_in.name,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def update(self, db: Session, db_obj: Category, obj_in: CategoryUpdate) -> Category:
    db_obj.name = obj_in.name
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def remove(self, db: Session, id: int) -> Category | None:
    obj = self.get(db, id)
    if obj:
      db.delete(obj)
      db.commit()
    return obj

category = CRUDCategory()
