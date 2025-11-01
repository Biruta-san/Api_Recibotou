from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import Dict, List, Tuple
from app.crud.entry import entry as crud_entry
from app.models.entry import Entry
from app.utils.enum import TipoLancamento

def get_entries_for_month(db: Session, user_id: int, month: int, year: int) -> Tuple[List[Entry], List[Entry]]:
  """Busca receitas e despesas para um mês/ano específicos de um usuário."""
  start_date = date(year, month, 1)
  # Lógica para achar o último dia do mês de forma segura
  next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
  end_date = next_month - timedelta(days=1)

  # Busca as receitas do mês para o usuário
  receitas = crud_entry.get_many_by_owner(
    db, user_id=user_id, entry_type_id=TipoLancamento.RECEITA, start_date=start_date, end_date=end_date
  )

  # Busca as despesas do mês para o usuário
  despesas = crud_entry.get_many_by_owner(
    db, user_id=user_id, entry_type_id=TipoLancamento.DESPESA, start_date=start_date, end_date=end_date
  )

  return receitas, despesas

def get_monthly_summary(db: Session, user_id: int, month: int, year: int) -> Dict[str, float]:
  """
  Calcula o resumo financeiro para um mês/ano, replicando a lógica do seu provedor Dart.
  """
  # 1. BUSCA DOS DADOS: Pega todos os lançamentos do mês para o usuário
  receitas, despesas = get_entries_for_month(db, user_id, month, year)

  # 2. CÁLCULO DOS TOTAIS (A LÓGICA DE NEGÓCIO)
  total_receitas = sum(entry.value for entry in receitas)
  total_despesas = sum(entry.value for entry in despesas)
  saldo_final = total_receitas - total_despesas

  # O saldo investido dependeria dos cofrinhos, que ainda não temos. Deixamos como 0.
  total_investido = 0.0

  # 3. RETORNO: Formata o resultado no dicionário esperado pelo router
  return {
    "totalReceitas": float(total_receitas),
    "totalDespesas": float(total_despesas),
    "totalInvestido": total_investido,
    "saldoDisponivel": float(saldo_final),
  }

# TODO: Criar as funções para Análise Anual e Cofrinhos aqui no futuro.
