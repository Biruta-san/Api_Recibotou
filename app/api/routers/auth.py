from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas.token import Token
from app.api.deps import get_db
from app.crud.user import user as crud_user
from app.core.security import verify_password, create_access_token
from app.utils.responses import ResponseModel, success_response, error_response
from app.core.config import settings
from app.schemas.auth import VerifyRequest, LoginRequest, ResetPasswordRequest, ResetPasswordRequest, VerifierOut
from fastapi import BackgroundTasks
from app.crud.user_auth import user_auth as crud_user_auth

router = APIRouter(tags=["auth"])

@router.post(
  "/request_login",
  response_model=ResponseModel[VerifierOut]
)
async def request_login(
  request: LoginRequest,
  background_tasks: BackgroundTasks,
  db: Session = Depends(get_db),
):
  db_user = crud_user.get_by_email(db, request.email)
  if not db_user or not verify_password(request.password, db_user.password):
    return error_response(
      error="Invalid credentials",
      message="Email ou senha incorretos.",
      status_code=status.HTTP_401_UNAUTHORIZED
    )

  verifier = await crud_user_auth.send_verification_email(
    db=db,
    user=db_user,
    background_tasks=background_tasks
  )

  if verifier is None:
    return error_response(
      error="Failed to send verification code",
      message="Falha ao enviar o código de verificação.",
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

  return success_response(
    data=VerifierOut(verifier=verifier),
    message="Código de autenticação gerado com sucesso.",
    status_code=status.HTTP_200_OK
  )

@router.post(
  "/login",
  response_model=ResponseModel[Token]
)
def login(
  request: VerifyRequest,
  db: Session = Depends(get_db),
):
  db_user_auth = crud_user_auth.get_by_verifier(db, request.verifier)
  if not db_user_auth:
    return error_response(
      error="Invalid verifier",
      message="Código de verificação inválido.",
      status_code=status.HTTP_401_UNAUTHORIZED
    )

  verified = crud_user_auth.verify_code(
    db=db,
    user_id=db_user_auth.user_id,
    verifier=request.verifier,
    code=request.code
  )

  if not verified:
    return error_response(
      error="Failed to verify code",
      message="Falha ao verificar o código.",
      status_code=status.HTTP_401_UNAUTHORIZED
    )

  access_token = create_access_token(
    data={"sub": str(db_user_auth.user_id)},
    expires_delta=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS),
  )

  return success_response(
    data=Token(access_token=access_token, token_type="bearer"),
    message="Login bem-sucedido.",
    status_code=status.HTTP_200_OK
  )

@router.post("/request_password_reset", response_model=ResponseModel[None])
async def request_password_reset(
  request: ResetPasswordRequest,
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

  await crud_user.generate_pass_recovery_token(
    db=db,
    db_obj=db_user,
    background_tasks=background_tasks)

  return success_response(
    data=None,
    message="E-mail de recuperação enviado com sucesso.",
    status_code=status.HTTP_200_OK
  )

@router.post("/reset_password", response_model=ResponseModel[None])
async def reset_password(
  request: ResetPasswordRequest,
  db: Session = Depends(get_db),
):
  if request.new_password != request.confirm_password:
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

  if not updated:
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
