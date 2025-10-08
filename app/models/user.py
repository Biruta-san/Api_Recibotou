# app/models/user.py (Versão Corrigida)

from sqlalchemy import String, Date
# <-- CORREÇÃO 1: Adicionar 'relationship' à importação
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from app.db.base import Base
from datetime import date
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.entry import Entry


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

    # <-- CORREÇÃO 2: Usar 'relationship()' em vez de 'mapped_column()'
    entries: Mapped[List["Entry"]] = relationship(back_populates="owner")