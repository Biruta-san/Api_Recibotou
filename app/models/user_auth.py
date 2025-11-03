from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, String
from datetime import datetime

class UserAuth(Base):
  __tablename__ = "user_auth"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
  code: Mapped[str] = mapped_column(String(255), nullable=False)
  verifier: Mapped[str] = mapped_column(String(255), nullable=False)
  expire_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
  updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

  user: Mapped["User"] = relationship(back_populates="auths")
