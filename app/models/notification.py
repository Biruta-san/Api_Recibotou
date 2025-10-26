from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, String
from datetime import datetime

class Notification(Base):
  __tablename__ = "notifications"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  message: Mapped[str | None] = mapped_column(String(500), nullable=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
  read: Mapped[bool] = mapped_column(default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

  user: Mapped["User"] = relationship(back_populates="notifications")

