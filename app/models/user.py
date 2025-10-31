# app/models/user.py (VERSÃO FINAL RESOLVIDA E COMPLETA)

from sqlalchemy import String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import date, datetime
from typing import List, TYPE_CHECKING
from sqlalchemy.dialects.mysql import MEDIUMBLOB # Tipo específico para MySQL

# Importações condicionais para evitar erros de importação circular
if TYPE_CHECKING:
    from app.models.entry import Entry
    from app.models.goal import Goal # Assumindo que o modelo de Metas exista
    from app.models.notification import Notification # Assumindo que o modelo de Notificações exista


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # --- CAMPOS OPCIONAIS E EXTRAS ---
    phone_number: Mapped[str | None] = mapped_column(String(20), unique=True, index=True, nullable=True)
    birthdate: Mapped[date | None] = mapped_column(Date, nullable=True)
    profession: Mapped[str | None] = mapped_column(String(100), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # --- CAMPOS DE RECUPERAÇÃO DE SENHA ---
    password_reset_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_reset_token_expiration: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # --- CAMPOS DE IMAGEM DE PERFIL (Para o blob de dados no MySQL) ---
    profile_image: Mapped[bytes | None] = mapped_column(MEDIUMBLOB, nullable=True)
    profile_image_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    profile_image_type: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # --- RELAÇÕES (PARA OUTRAS TABELAS) ---
    # Relação com Lançamentos (a que corrigimos)
    entries: Mapped[List["Entry"]] = relationship(back_populates="owner") # Aqui usamos "owner" para ser consistente com Entry.py
    
    # Relação com Metas
    goals: Mapped[List["Goal"]] = relationship(back_populates="user")
    
    # Relação com Notificações
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user")