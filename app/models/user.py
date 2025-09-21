from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from datetime import date

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
  full_name: Mapped[str] = mapped_column(String(255), nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  phone_number: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=True)
  birthdate: Mapped[date] = mapped_column(Date, nullable=True)
  profession: Mapped[str] = mapped_column(String(100), nullable=True)
  address: Mapped[str] = mapped_column(String(255), nullable=True)
  city: Mapped[str] = mapped_column(String(100), nullable=True)
