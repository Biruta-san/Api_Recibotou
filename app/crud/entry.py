from sqlalchemy.orm import Session
from datetime import date
from typing import Optional, List
from sqlalchemy import func
from decimal import Decimal
from app.utils.enum import TipoLancamento
from app.models.entry import Entry
from app.schemas.entry import EntryCreate, EntryUpdate

class CRUDEntry:
  def get(self, db: Session, id: int) -> Optional[Entry]:
    return db.get(Entry, id)

  def get_many(
    self,
    db: Session,
    title: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    user_id: Optional[int] = None,
    category_id: Optional[int] = None,
    entry_type_id: Optional[int] = None,
  ) -> List[Entry]:
    query = db.query(Entry)

    if title:
      query = query.filter(func.lower(Entry.title).like(f"%{title.lower()}%"))
    if start_date:
      query = query.filter(Entry.entry_date >= start_date)
    if end_date:
      query = query.filter(Entry.entry_date <= end_date)
    if user_id:
      query = query.filter(Entry.user_id == user_id)
    if category_id:
      query = query.filter(Entry.category_id == category_id)
    if entry_type_id:
      query = query.filter(Entry.entry_type_id == entry_type_id)

    # Ordena pelo mais recente para ter uma listagem consistente
    return query.order_by(Entry.entry_date.desc()).all()


  def get_many_by_owner(
    self,
    db: Session,
    user_id: int,
    title: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    entry_type_id: Optional[int] = None,
  ) -> List[Entry]:
    """
    Busca múltiplos lançamentos APENAS do usuário logado (usado em todas as rotas GET).
    """
    query = db.query(Entry).filter(Entry.user_id == user_id) # FILTRO DE SEGURANÇA

    if title:
        query = query.filter(func.lower(Entry.title).like(f"%{title.lower()}%"))
    if start_date:
        query = query.filter(Entry.entry_date >= start_date)
    if end_date:
        query = query.filter(Entry.entry_date <= end_date)
    if category_id:
        query = query.filter(Entry.category_id == category_id)
    if entry_type_id:
        query = query.filter(Entry.entry_type_id == entry_type_id)

    return query.order_by(Entry.entry_date.desc()).all()


  def create(self, db: Session, obj_in: EntryCreate) -> Entry:
    db_obj = Entry(
      title=obj_in.title,
      entry_date=obj_in.entry_date,
      description=obj_in.description,
      value=obj_in.value,
      entry_type_id=obj_in.entry_type_id,
      category_id=obj_in.category_id,
      user_id=obj_in.user_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def create_with_owner(self, db: Session, obj_in: EntryCreate, user_id: int) -> Entry:
    """
    Cria um novo lançamento garantindo que o usuário seja o dono. (Nosso padrão)
    """
    # Garantindo que o user_id passado na função sobrescreva qualquer valor que venha no schema.
    data_dict = obj_in.model_dump(exclude={'user_id'})

    db_obj = Entry(
      **data_dict,
      user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


  def update(self, db: Session, db_obj: Entry, obj_in: EntryUpdate) -> Entry:
    db_obj.title = obj_in.title
    db_obj.entry_date = obj_in.entry_date
    db_obj.description = obj_in.description
    db_obj.value = obj_in.value
    db_obj.entry_type_id = obj_in.entry_type_id
    db_obj.category_id = obj_in.category_id
    db_obj.user_id = obj_in.user_id

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


  def get_sum_by_period(
    self,
    db: Session,
    month: int,
    year: int,
    user_id: int,
    category_id: Optional[int] = None
  ) -> Decimal:
    query = db.query(Entry).filter(
      func.month(Entry.entry_date) == month,
      func.year(Entry.entry_date) == year,
      Entry.entry_type_id == TipoLancamento.DESPESA,
      Entry.user_id == user_id
    )

    if category_id is not None:
      query = query.filter(Entry.category_id == category_id)

    total = query.with_entities(func.sum(Entry.value)).scalar()
    return Decimal(total) if total is not None else Decimal(0)

  def remove(self, db: Session, id: int) -> Optional[Entry]:
    obj = self.get(db, id)
    if obj:
      db.delete(obj)
      db.commit()
    return obj

entry = CRUDEntry()
