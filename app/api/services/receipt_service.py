from sqlalchemy.orm import Session
from fastapi import UploadFile
from datetime import date
import re
from app.api.services import ocr_service
from app.crud.entry import entry as entry_crud
from app.schemas.entry import EntryCreate
from app.models.entry import Entry

async def process_receipt_image(db: Session, user_id: int, file: UploadFile) -> Entry:
  """
  Orquestra o processo de validação de recibo:
  1. Lê o conteúdo do arquivo.
  2. Usa o ocr_service para extrair o texto.
  3. Analisa o texto para extrair informações (valor, tipo).
  4. Cria o lançamento no banco de dados usando o CRUD.
  """
  image_content = await file.read()

  # Passo 1: Extrair dados da imagem usando o serviço reutilizado
  try:
    ocr_results = ocr_service.extract_text_from_image_content(image_content)
  except Exception as e:
    raise ValueError(f"Falha ao processar a imagem com OCR: {e}")

  if not ocr_results:
    raise ValueError("Não foi possível extrair texto do recibo. A imagem pode estar ilegível.")

  # Concatena todo o texto detectado em uma única string para análise
  extracted_text = " ".join([item['text'] for item in ocr_results])

  # --- NOSSAS LINHAS DE DEPURAÇÃO ---
  #print("--- TEXTO EXTRAÍDO PELO OCR ---")
  #print(extracted_text)
  #print("---------------------------------")
  # ------------------------------------

  # Passo 2: Analisar o texto (NLP Simples)
  # <-- CORREÇÃO 2: Usar a variável correta 'extracted_text'
  full_text_lower = extracted_text.lower()

  # 2.1 Identificar o tipo (entrada ou saída)
  entry_type_id = 2  # Padrão: Saída (despesa)
  keywords_entrada = ['pix recebido', 'salário', 'depósito', 'crédito', 'recebimento']
  # <-- CORREÇÃO 3: Corrigir erro de digitação '.lowe' e usar a variável correta
  if any(keyword in full_text_lower for keyword in keywords_entrada):
    entry_type_id = 1  # Entrada (receita)

  # 2.2 Identificar o valor
  match = re.search(r'(?:r\$|rs)\s*([\d.,]+)', full_text_lower)
  if not match:
    raise ValueError("Não foi possível identificar um valor monetário no recibo.")

  value_str = match.group(1).replace('.', '').replace(',', '.')
  value = float(value_str)

  # 2.3 Montar o objeto completo
  # <-- CORREÇÃO 4: Adicionar os campos obrigatórios 'title' e 'entry_date'
  entry_data = EntryCreate(
    title="Lançamento via Recibo",
    entry_date=date.today(),
    description=f"Lançamento automático via recibo: {extracted_text[:100]}...",
    value=value,
    entry_type_id=entry_type_id
  )

  # Passo 3: Salvar no banco usando a função correta do CRUD
  created_entry = entry_crud.create_with_owner(db=db, obj_in=entry_data, user_id=user_id)
  return created_entry
