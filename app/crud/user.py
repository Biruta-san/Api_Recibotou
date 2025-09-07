from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class CRUDUser:
  def get(self, db: Session, id: int) -> User | None:
    return db.get(User, id)


  def get_by_email(self, db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


  def create(self, db: Session, obj_in: UserCreate) -> User:
    db_obj = User(email=obj_in.email, full_name=obj_in.full_name, password=get_password_hash(obj_in.password))
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


  def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
    db_obj.full_name = obj_in.full_name
    db_obj.email = obj_in.email

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


  def remove(self, db: Session, id: int) -> User | None:
    obj = self.get(db, id)
    if obj:
      db.delete(obj)
      db.commit()
    return obj


user = CRUDUser()