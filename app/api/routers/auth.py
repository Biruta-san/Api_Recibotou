from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas.token import Token
from app.api.deps import get_db
from app.crud.user import user as crud_user
from app.core.security import verify_password, create_access_token
from app.utils.responses import ResponseModel, success_response, error_response
from app.core.config import settings
from app.schemas.user import LoginRequest

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=ResponseModel[Token])
def login(request: LoginRequest, db: Session = Depends(get_db)):
  db_user = crud_user.get_by_email(db, request.email)
  if not db_user or not verify_password(request.password, db_user.password):
    return error_response(
      error="Invalid credentials",
      message="Email ou senha incorretos.",
      status_code=status.HTTP_401_UNAUTHORIZED
    )

  access_token = create_access_token(
    data={"sub": str(db_user.id)},
    expires_delta=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS),
  )

  return success_response(
    data={"access_token": access_token, "token_type": "bearer"},
    message="Login bem-sucedido.",
    status_code=status.HTTP_200_OK
  )
