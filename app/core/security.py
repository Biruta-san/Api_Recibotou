from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
import base64
from cryptography.fernet import Fernet

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
  return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  expire = datetime.utcnow() + (expires_delta or timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS))
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ENCODING_ALGORITHM)
  return encoded_jwt

def _get_fernet() -> Fernet:
  """
  Cria uma instância do Fernet a partir da SECRET_KEY do .env.
  A chave precisa ter 32 bytes e ser codificada em base64.
  """
  key = settings.SECRET_KEY.encode()

  # Garante que a chave tenha o formato válido exigido pelo Fernet
  key_32 = base64.urlsafe_b64encode(key.ljust(32, b"0")[:32])

  return Fernet(key_32)

def encrypt_data(data: str) -> str:
  """
  Criptografa uma string usando a SECRET_KEY do ambiente.
  """
  fernet = _get_fernet()
  encrypted = fernet.encrypt(data.encode())
  return encrypted.decode()


def decrypt_data(token: str) -> str:
  """
  Descriptografa uma string usando a SECRET_KEY do ambiente.
  """
  fernet = _get_fernet()
  decrypted = fernet.decrypt(token.encode())
  return decrypted.decode()
