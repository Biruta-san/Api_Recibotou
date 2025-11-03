from pydantic import BaseModel, EmailStr
from datetime import date

class UserBase(BaseModel):
  email: EmailStr
  full_name: str
  phone_number: str
  birthdate: date
  profession: str
  address: str
  city: str

class UserCreate(UserBase):
  password: str

class UserUpdate(UserBase):
  pass

class UserOut(UserBase):
  id: int

  class Config:
    from_attributes = True

