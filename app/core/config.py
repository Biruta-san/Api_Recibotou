from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  API_V1_STR: str = "/api/v1"
  PROJECT_NAME: str = "Nome do Projeto"
  SECRET_KEY: str = "chave_de_criptografia"
  ACCESS_TOKEN_EXPIRE_DAYS: int = 5
  # URL exemplo com PyMySQL
  SQLALCHEMY_DATABASE_URI: str = (
  "mysql+pymysql://user:password@localhost:3306/minha_api"
  )
  ENCODING_ALGORITHM: str = "HS256"

  GOOGLE_API_KEY: str | None = None

  # CORS
  BACKEND_CORS_ORIGINS: list[str] = ["*"]
  SMTP_SERVER: str | None = None
  SMTP_PORT: int | None = None
  SMTP_USERNAME: str | None = None
  SMTP_PASSWORD: str | None = None
  SMTP_FROM: str | None = None

  API_HOST: str = "0.0.0.0"
  API_PORT: int = 8000
  APP_URL: str = "https://0.0.0.0:8000"

  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
