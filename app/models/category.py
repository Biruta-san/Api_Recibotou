from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class Category(Base):
  __tablename__ = "categories"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)

  entries: Mapped[list["Entry"]] = relationship(back_populates="category")
  goals: Mapped[list["Goal"]] = relationship(back_populates="category")
