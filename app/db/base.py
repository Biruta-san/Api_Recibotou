from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

from app.models import user, goal, entry, category, entry_type
