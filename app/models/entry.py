# app/models/entry.py (Versão Corrigida)

from sqlalchemy import String, ForeignKey, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.entry_type import EntryType
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

# <-- ADIÇÃO 1: Para evitar erros de importação circular
if TYPE_CHECKING:
    from app.models.user import User


class Entry(Base):
    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    entry_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    entry_type_id: Mapped[int] = mapped_column(ForeignKey("entry_types.id"), nullable=False, index=True)

    # --- LINHAS ADICIONADAS ---
    # <-- ADIÇÃO 2: A coluna que guarda o ID do dono do lançamento
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    
    # <-- ADIÇÃO 3: A "relação" que nos permite acessar o objeto User a partir de um Entry
    owner: Mapped["User"] = relationship(back_populates="entries")
    # --------------------------

    entry_type: Mapped["EntryType"] = relationship(back_populates="entries")