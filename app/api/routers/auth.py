from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas.token import Token
from app.api.deps import get_db
from app.crud.user import user as crud_user
from app.core.security import verify_password, create_access_token
from app.utils.responses import ResponseModel, success_response, error_response
from app.core.config import settings
from app.schemas.user import LoginRequest, ResetPasswordRequest, RequestResetPasswordRequest
from fastapi import BackgroundTasks

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

@router.post("/requestPasswordReset", response_model=ResponseModel[None])
async def request_password_reset(
  request: RequestResetPasswordRequest,
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db),
):
  db_user = crud_user.get_by_email(db, request.email)

  if not db_user:
    return error_response(
      error="User not found",
      message="Usuário não encontrado.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  access_token = await crud_user.generate_pass_recovery_token(
    db=db,
    db_obj=db_user,
    background_tasks=background_tasks)

  return success_response(
    data=None,
    message="Login bem-sucedido.",
    status_code=status.HTTP_200_OK
  )

@router.post("/resetPassword", response_model=ResponseModel[None])
async def reset_password(
  request: ResetPasswordRequest,
  db: Session = Depends(get_db),
):
  if(request.new_password != request.confirm_password):
    return error_response(
      error="Password mismatch",
      message="As senhas não coincidem.",
      status_code=status.HTTP_400_BAD_REQUEST
    )

  db_user = crud_user.get_by_email(db, request.email)

  if not db_user:
    return error_response(
      error="User not found",
      message="Usuário não encontrado.",
      status_code=status.HTTP_404_NOT_FOUND
    )

  updated = crud_user.verify_token_and_update_password(db=db, db_obj=db_user, new_password=request.new_password, token=request.token)

  if(not updated):
    return error_response(
      error="Invalid or expired token",
      message="Token inválido ou expirado.",
      status_code=status.HTTP_400_BAD_REQUEST
    )

  return success_response(
    data=None,
    message="Senha redefinida com sucesso.",
    status_code=status.HTTP_200_OK
  )
