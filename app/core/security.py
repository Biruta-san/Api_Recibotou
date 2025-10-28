from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
import base64
import hashlib
from cryptography.fernet import Fernet

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
  return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  expire = datetime.now() + (expires_delta or timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS))
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ENCODING_ALGORITHM)
  return encoded_jwt

def _get_fernet() -> Fernet:
  """
  Cria um objeto Fernet derivando a chave secreta do settings.SECRET_KEY.
  Garante que a chave tenha o tamanho correto (32 bytes, codificada em base64).
  """
  key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
  key_b64 = base64.urlsafe_b64encode(key)
  return Fernet(key_b64)


def encrypt_data(data: str) -> str:
  """
  Criptografa uma string e retorna o texto criptografado (base64).
  """
  fernet = _get_fernet()
  encrypted = fernet.encrypt(data.encode())
  return encrypted.decode()


def decrypt_data(token: str) -> str:
  """
  Descriptografa um texto criptografado (base64) e retorna a string original.
  """
  fernet = _get_fernet()
  decrypted = fernet.decrypt(token.encode())
  return decrypted.decode()
