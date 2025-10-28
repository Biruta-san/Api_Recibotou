<<<<<<< HEAD
# app/models/user.py (Versão Corrigida)

from sqlalchemy import String, Date
<<<<<<< HEAD
# <-- CORREÇÃO 1: Adicionar 'relationship' à importação
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from app.db.base import Base
from datetime import date
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.entry import Entry

=======
from sqlalchemy import String, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import date, datetime
from sqlalchemy.dialects.mysql import MEDIUMBLOB
>>>>>>> origin/main
=======
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import date
>>>>>>> 7dc122e3ab86853868dc347cecc7855854553682

class User(Base):
  __tablename__ = "users"

<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
>>>>>>> 7dc122e3ab86853868dc347cecc7855854553682
  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
  full_name: Mapped[str] = mapped_column(String(255), nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  phone_number: Mapped[str | None] = mapped_column(String(20), unique=True, index=True, nullable=True)
  birthdate: Mapped[date | None] = mapped_column(Date, nullable=True)
  profession: Mapped[str | None] = mapped_column(String(100), nullable=True)
  address: Mapped[str | None] = mapped_column(String(255), nullable=True)
  city: Mapped[str | None] = mapped_column(String(100), nullable=True)

  password_reset_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
  password_reset_token_expiration: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

  profile_image: Mapped[bytes | None] = mapped_column(MEDIUMBLOB, nullable=True)
  profile_image_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
  profile_image_type: Mapped[str | None] = mapped_column(String(255), nullable=True)

  goals: Mapped[list["Goal"]] = relationship(back_populates="user")
  entries: Mapped[list["Entry"]] = relationship(back_populates="user")
<<<<<<< HEAD
  notifications: Mapped[list["Notification"]] = relationship(back_populates="user")
>>>>>>> origin/main
=======
>>>>>>> 7dc122e3ab86853868dc347cecc7855854553682
