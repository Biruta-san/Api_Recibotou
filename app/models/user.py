from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import date

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
  full_name: Mapped[str] = mapped_column(String(255), nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  phone_number: Mapped[str | None] = mapped_column(String(20), unique=True, index=True, nullable=True)
  birthdate: Mapped[date | None] = mapped_column(Date, nullable=True)
  profession: Mapped[str | None] = mapped_column(String(100), nullable=True)
  address: Mapped[str | None] = mapped_column(String(255), nullable=True)
  city: Mapped[str | None] = mapped_column(String(100), nullable=True)

  goals: Mapped[list["Goal"]] = relationship(back_populates="user")
  entries: Mapped[list["Entry"]] = relationship(back_populates="user")
