from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

# Importações centralizadas
from app.db.session import get_db
from app.core.config import settings
from app.crud.user import user as crud_user
from app.models.user import User

# O HTTPBearer é mais simples e funciona perfeitamente para extrair o token
security = HTTPBearer()

def get_current_active_user(
    credentials=Depends(security), db: Session = Depends(get_db)
) -> User:
    """
    Valida o token do cabeçalho, busca o usuário pelo ID 
    e verifica se ele está ativo.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token usando a chave secreta do projeto
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Pega o ID do usuário do "subject" do token
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValueError):
        # Captura erros de token inválido ou se o 'sub' não for um número
        raise credentials_exception

    # Busca o usuário no banco pelo ID
    user = crud_user.get(db, id=user_id)
    if user is None:
        raise credentials_exception

    # MELHORIA: Verifica se o usuário está ativo
    # (Assumindo que seu modelo User tem um campo booleano 'is_active')
    # if not user.is_active:
    #     raise HTTPException(status_code=403, detail="Usuário inativo")

    return user