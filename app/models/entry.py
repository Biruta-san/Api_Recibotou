# app/models/entry.py (VERSÃO FINAL RESOLVIDA E COMPLETA)

from sqlalchemy import String, ForeignKey, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

# Importações condicionais para evitar erros de importação circular
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.category import Category # Assumindo que a tabela de categorias é chamada 'Category'
    from app.models.entry_type import EntryType


class Entry(Base):
    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    entry_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    
    # --- CHAVES ESTRANGEIRAS (COLUNAS) ---
    entry_type_id: Mapped[int] = mapped_column(ForeignKey("entry_types.id"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True, index=True) # Assumindo categories.id
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    
    # --- RELAÇÕES (ATALHOS DO PYTHON) ---
    # Relação com o tipo de lançamento (Receita/Despesa)
    entry_type: Mapped["EntryType"] = relationship(back_populates="entries") 
    
    # Relação com a categoria (Do código do seu colega)
    category: Mapped["Category"] = relationship(back_populates="entries") 
    
    # Relação com o dono do lançamento (owner)
    owner: Mapped["User"] = relationship(back_populates="entries")