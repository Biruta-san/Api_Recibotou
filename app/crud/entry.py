# app/crud/entry.py (Versão Corrigida e Segura)

from sqlalchemy.orm import Session
<<<<<<< HEAD
from sqlalchemy import func
from datetime import date
from typing import Optional, List

from app.models.entry import Entry
from app.schemas.entry import EntryCreate, EntryUpdate
=======
from app.models.entry import Entry
from app.schemas.entry import EntryCreate, EntryUpdate
from datetime import date
from typing import Optional
from sqlalchemy import func
from app.utils.enum import TipoLancamento
from decimal import Decimal
>>>>>>> origin/main

class CRUDEntry:
    def get(self, db: Session, id: int) -> Optional[Entry]:
        return db.get(Entry, id)

<<<<<<< HEAD
    def get_many(
        self,
        db: Session,
        title: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Entry]:
        """
        Busca múltiplos lançamentos no banco. 
        AVISO: Esta função busca em TODOS os lançamentos, sem filtro de usuário.
        """
        query = db.query(Entry)

        if title:
            # filtro case-insensitive
            query = query.filter(func.lower(Entry.title).like(f"%{title.lower()}%"))
        if start_date:
            query = query.filter(Entry.entry_date >= start_date)
        if end_date:
            query = query.filter(Entry.entry_date <= end_date)
=======
  def get_many(
    self,
    db: Session,
    title: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    user_id: Optional[int] = None,
    category_id: Optional[int] = None,
    entry_type_id: Optional[int] = None,
  ):
    query = db.query(Entry)

    if title:
      query = query.filter(func.lower(Entry.title).like(f"%{title.lower()}%"))
>>>>>>> origin/main

        return query.all()

    # <-- FUNÇÃO ADICIONADA PARA SEGURANÇA E LÓGICA CORRETA
    def get_many_by_owner(
        self,
        db: Session,
        user_id: int,
        title: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Entry]:
        """
        Busca múltiplos lançamentos pertencentes a um usuário específico.
        """
        # A linha mais importante: filtra apenas os lançamentos do usuário logado
        query = db.query(Entry).filter(Entry.user_id == user_id)

<<<<<<< HEAD
        if title:
            query = query.filter(func.lower(Entry.title).like(f"%{title.lower()}%"))
        if start_date:
            query = query.filter(Entry.entry_date >= start_date)
        if end_date:
            query = query.filter(Entry.entry_date <= end_date)
        
        # Ordena do mais recente para o mais antigo
        return query.order_by(Entry.entry_date.desc()).all()

    def create(self, db: Session, obj_in: EntryCreate) -> Entry:
        """
        Cria um lançamento sem um dono. 
        (Manter para possíveis usos administrativos, mas evitar em rotas de usuário).
        """
        db_obj = Entry(
            title=obj_in.title,
            entry_date=obj_in.entry_date,
            description=obj_in.description,
            value=obj_in.value,
            entry_type_id=obj_in.entry_type_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def create_with_owner(self, db: Session, obj_in: EntryCreate, user_id: int) -> Entry:
        """
        Cria um novo lançamento no banco de dados e o associa a um usuário.
        """
        db_obj = Entry(
            **obj_in.model_dump(),  # Copia todos os dados do schema
            user_id=user_id       # Adiciona o ID do dono
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Entry, obj_in: EntryUpdate) -> Entry:
        # Pega os dados do schema como um dicionário
        update_data = obj_in.model_dump(exclude_unset=True)
        # Atualiza os campos do objeto do banco com os dados do dicionário
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
=======
    if user_id:
      query = query.filter(Entry.user_id == user_id)

    if category_id:
      query = query.filter(Entry.category_id == category_id)

    if entry_type_id:
      query = query.filter(Entry.entry_type_id == entry_type_id)

    return query.all()

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

  def update(self, db: Session, db_obj: Entry, obj_in: EntryUpdate) -> Entry:
    db_obj.title = obj_in.title
    db_obj.entry_date = obj_in.entry_date
    db_obj.description = obj_in.description
    db_obj.value = obj_in.value
    db_obj.entry_type_id = obj_in.entry_type_id
    db_obj.category_id = obj_in.category_id
    db_obj.user_id = obj_in.user_id
>>>>>>> origin/main

    def remove(self, db: Session, id: int) -> Optional[Entry]:
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

<<<<<<< HEAD
entry = CRUDEntry()
=======
  def remove(self, db: Session, id: int) -> Entry | None:
    obj = self.get(db, id)
    if obj:
      db.delete(obj)
      db.commit()
    return obj

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
      Entry.user_id == user_id)

    if category_id is not None:
      query = query.filter(Entry.category_id == category_id)

    total = query.with_entities(func.sum(Entry.value)).scalar()
    return Decimal(total or 0.0)

entry = CRUDEntry()
>>>>>>> origin/main
