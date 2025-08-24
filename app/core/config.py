from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  API_V1_STR: str = "/api/v1"
  PROJECT_NAME: str = "Minha API"


  # URL exemplo com PyMySQL
  SQLALCHEMY_DATABASE_URI: str = (
  "mysql+pymysql://user:password@localhost:3306/minha_api"
  )


  # CORS
  BACKEND_CORS_ORIGINS: list[str] = ["*"]


  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()