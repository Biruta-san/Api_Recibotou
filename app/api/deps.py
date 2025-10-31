from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.config import settings
from app.crud.user import user as crud_user
from app.models.user import User

security = HTTPBearer()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def get_current_user(credentials=Depends(security), db: Session = Depends(get_db)) -> User:
  token = credentials.credentials
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )

  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id: int = int(payload.get("sub"))
    if user_id is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception

  user = crud_user.get(db, user_id)
  if user is None:
    raise credentials_exception
  return user
