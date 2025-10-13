from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import SmallInteger, ForeignKey, CheckConstraint, Index, Numeric
from sqlalchemy.dialects.mysql import YEAR
from app.models.user import User
from app.models.category import Category
from decimal import Decimal

class Goal(Base):
  __tablename__ = "goals"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  month: Mapped[int] = mapped_column(SmallInteger, nullable=False)
  year: Mapped[int] = mapped_column(YEAR, nullable=False)
  value: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
  category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True, index=True)

  __table_args__ = (
        CheckConstraint("month BETWEEN 1 AND 12", name="check_valid_month"),
        Index("idx_payments_year_month", "year", "month"),
    )

  user: Mapped["User"] = relationship(back_populates="goals")
  category: Mapped["Category"] = relationship(back_populates="goals")
