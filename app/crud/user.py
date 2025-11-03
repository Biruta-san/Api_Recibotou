from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, encrypt_data, decrypt_data
import secrets
from app.core.mail import send_password_recovery_email
from datetime import datetime, timedelta
from fastapi import BackgroundTasks

class CRUDUser:
  def get(self, db: Session, id: int) -> User | None:
    return db.get(User, id)

  def get_by_email(self, db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

  def get_by_phone(self, db: Session, phone: str) -> User | None:
    return db.query(User).filter(User.phone_number == phone).first()

  def create(self, db: Session, obj_in: UserCreate) -> User:
    db_obj = User(
      email=obj_in.email,
      full_name=obj_in.full_name,
      password=get_password_hash(obj_in.password),
      phone_number=obj_in.phone_number,
      birthdate=obj_in.birthdate,
      profession=obj_in.profession,
      address=obj_in.address,
      city=obj_in.city,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


  def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
    db_obj.full_name = obj_in.full_name
    db_obj.email = obj_in.email
    db_obj.phone_number = obj_in.phone_number
    db_obj.birthdate = obj_in.birthdate
    db_obj.profession = obj_in.profession
    db_obj.address = obj_in.address
    db_obj.city = obj_in.city

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

  async def generate_pass_recovery_token(
    self,
    db: Session,
    db_obj: User,
    background_tasks: BackgroundTasks
  ) -> str:
    token = secrets.token_hex(3).upper()
    date_expiration = datetime.now() + timedelta(minutes=5)

    db_obj.password_reset_token = encrypt_data(token)
    db_obj.password_reset_token_expiration = date_expiration

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    background_tasks.add_task(send_password_recovery_email, db_obj.email, token, date_expiration)

    return token

  def verify_token_and_update_password(self, db: Session, db_obj: User, token: str, new_password: str) -> bool:
    if (
      decrypt_data(db_obj.password_reset_token) == token and
      db_obj.password_reset_token_expiration and
      db_obj.password_reset_token_expiration >= datetime.now()
    ):
      db_obj.password_reset_token = None
      db_obj.password_reset_token_expiration = None
      db_obj.password = get_password_hash(new_password)
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return True
    return False

  def update_profile_image(self, db: Session, db_obj: User, image_data: bytes, image_name: str, image_type: str) -> User:
    db_obj.profile_image = image_data
    db_obj.profile_image_name = image_name
    db_obj.profile_image_type = image_type
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


user = CRUDUser()
