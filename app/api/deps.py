from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

# Importações centrais
from app.db.session import get_db
from app.core.config import settings
from app.crud.user import user as crud_user  # Presume que o CRUD de usuário se chame 'crud_user'
from app.models.user import User


# ========================
# Configuração de segurança
# ========================

# OAuth2PasswordBearer é usado para exibir a autenticação no Swagger UI
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

# HTTPBearer é usado para realmente capturar o token do cabeçalho Authorization: Bearer <token>
security = HTTPBearer()


# ==========================
# Função principal de usuário
# ==========================

async def get_current_active_user(
    credentials=Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Valida o token JWT recebido no cabeçalho Authorization e retorna o usuário autenticado.
    """

    token = credentials.credentials

    # Exceção padrão para falha de autenticação
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token JWT usando a SECRET_KEY e o ALGORITHM definidos no projeto
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        # O campo 'sub' do token deve conter o ID do usuário
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception

    except (JWTError, ValueError):
        # Captura tokens inválidos, expirados ou com formato incorreto
        raise credentials_exception

    # Busca o usuário no banco de dados
    user = crud_user.get(db, id=user_id)
    if user is None:
        raise credentials_exception

    # Se o modelo tiver campo `is_active`, pode validar aqui
    # if not user.is_active:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")

    return user


# =================================================
# Alias para compatibilidade com o restante do app
# =================================================

# Muitos módulos podem ainda importar `get_current_user`.
# Este alias garante compatibilidade sem precisar mudar outros arquivos.
get_current_user = get_current_active_user
