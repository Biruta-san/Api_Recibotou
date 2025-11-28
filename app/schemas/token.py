from pydantic import BaseModel

class UserLogin(BaseModel):
  access_token: str
  token_type: str = "bearer"
  user_id: int
  user_name: str
  user_email: str

class TokenData(BaseModel):
  sub: int | None = None

