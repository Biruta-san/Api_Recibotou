from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
  email: EmailStr
  full_name: str

class UserCreate(UserBase):
  password: str

class UserUpdate(UserBase):
  pass

class UserOut(UserBase):
  id: int

  class Config:
    from_attributes = True # pydantic v2