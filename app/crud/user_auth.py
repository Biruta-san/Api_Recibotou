from app.models.user_auth import UserAuth
from sqlalchemy.orm import Session
from app.models.user import User
import secrets
from datetime import datetime, timedelta
import uuid
from fastapi import BackgroundTasks
from app.core.mail import send_two_factor_code
from app.core.logger_config import logger
from app.core.security import encrypt_data, decrypt_data

class CRUDUserAuth:
  def get_by_verifier(
    self,
    db:Session,
    verifier: str
  ) -> UserAuth | None:
    return db.query(UserAuth).filter(UserAuth.verifier == verifier).first()

  async def send_verification_email(
    self,
    db: Session,
    user: User,
    background_tasks: BackgroundTasks
  ) -> str | None:
    try:
      code = secrets.token_hex(3).upper()
      encrypted_code = encrypt_data(code)
      date_expiration = datetime.now() + timedelta(minutes=5)
      verifier = str(uuid.uuid4())

      user_auth = db.query(UserAuth).filter(UserAuth.user_id == user.id).first()

      if user_auth is not None:
        user_auth.code = encrypted_code
        user_auth.expire_date = date_expiration
        user_auth.updated_at = datetime.now()
        user_auth.verifier = verifier
      else:
        user_auth = UserAuth(
          user_id=user.id,
          code=encrypted_code,
          verifier=verifier,
          expire_date=date_expiration,
        )

      db.add(user_auth)
      db.commit()
      db.refresh(user_auth)

      background_tasks.add_task(send_two_factor_code, user.email, code, date_expiration)

      return verifier
    except Exception as e:
      logger.error(f"Error sending verification email: {e}")
      return None

  def verify_code(
    self,
    db: Session,
    user_id: int,
    verifier: str,
    code: str
  ) -> bool:
    user_auth = db.query(UserAuth).filter(
      UserAuth.user_id == user_id,
      UserAuth.verifier == verifier,
      UserAuth.expire_date >= datetime.now()
    ).first()

    if not user_auth:
      return False

    return decrypt_data(user_auth.code) == code

user_auth = CRUDUserAuth()
