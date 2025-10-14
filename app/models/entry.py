from sqlalchemy import String, ForeignKey, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.entry_type import EntryType
from app.models.category import Category
from app.models.user import User
from datetime import date
from decimal import Decimal

class Entry(Base):
  __tablename__ = "entries"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  entry_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
  description: Mapped[str] = mapped_column(String(500), nullable=False)
  value: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
  entry_type_id: Mapped[int] = mapped_column(ForeignKey("entry_types.id"), nullable=False, index=True)
  category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False, index=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

  entry_type: Mapped["EntryType"] = relationship(back_populates="entries")
  category: Mapped["Category"] = relationship(back_populates="entries")
  user: Mapped["User"] = relationship(back_populates="entries")
