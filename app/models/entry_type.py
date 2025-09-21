from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from sqlalchemy import String

class EntryType(Base):
  __tablename__ = "entry_types"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)

  # relação inversa
  entries: Mapped[list["Entry"]] = relationship(back_populates="entry_type")
