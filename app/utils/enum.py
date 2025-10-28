from enum import IntEnum

class TipoLancamento(IntEnum):
  RECEITA = 1
  DESPESA = 2

class Categoria(IntEnum):
  ALIMENTACAO = 1
  TRANSPORTE = 2
  ENTRETENIMENTO = 3
  SAUDE = 4
  EDUCACAO = 5
  CASA = 6
  ROUPAS = 7
  OUTROS = 8
