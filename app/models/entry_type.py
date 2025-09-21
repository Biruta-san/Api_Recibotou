from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from sqlalchemy import String

class EntryType(Base):
  __tablename__ = "entry_type"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)