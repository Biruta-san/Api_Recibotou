from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
  email: EmailStr
  password: str

class VerifyRequest(BaseModel):
  verifier: str
  code: str

class VerifierOut(BaseModel):
  verifier: str

class ResetPasswordRequest(BaseModel):
  email: str

class ResetPasswordRequest(BaseModel):
  email: str
  new_password: str
  confirm_password: str
  token: str
