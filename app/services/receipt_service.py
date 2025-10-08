# app/api/services/receipt_service.py

from sqlalchemy.orm import Session
from fastapi import UploadFile
from datetime import date
import re

# Importa os módulos que vamos usar
from app.api.services import ocr_service
from app.crud.entry import entry as entry_crud
from app.schemas.entry import EntryCreate
from app.models.entry import Entry 

def process_receipt_image(db: Session, user_id: int, file: UploadFile) -> Entry:
    """
    Orquestra o processo de converter a imagem de um recibo em um lançamento no banco.
    """
    # 1. Lê a imagem e extrai o texto usando nosso serviço de OCR
    image_content = file.read()
    ocr_results = ocr_service.extract_text_from_image_content(image_content)
    
    if not ocr_results:
        raise ValueError("O recibo está ilegível e nenhum texto pôde ser extraído.")

    full_text = " ".join([item['text'] for item in ocr_results])
    full_text_lower = full_text.lower()

    # 2. Analisa o texto para encontrar o valor e o tipo de lançamento
    
    # Procura por um valor monetário (ex: R$ 50,00, 50.00, 50,00)
    match = re.search(r'r?\$\s*(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})', full_text_lower)
    if not match:
        raise ValueError("Não foi possível encontrar um valor monetário no recibo.")
    
    value_str = match.group(1).replace('.', '').replace(',', '.')
    value = float(value_str)

    # Define se é entrada ou saída baseado em palavras-chave.
    # Assumimos que no banco: entry_type_id=1 é 'Saída' e id=2 é 'Entrada'.
    entry_type_id = 1 # Padrão é Saída/Despesa
    income_keywords = ['pix recebido', 'salário', 'depósito', 'crédito', 'recebimento']
    if any(keyword in full_text_lower for keyword in income_keywords):
        entry_type_id = 2 # É Entrada/Receita
        
    # 3. Monta o objeto de criação (schema) com os dados extraídos
    entry_to_create = EntryCreate(
        title=f"Lançamento via Recibo",
        entry_date=date.today(),
        description=f"Lançamento automático via recibo: {full_text[:100]}...",
        value=value,
        entry_type_id=entry_type_id
    )

    # 4. Salva o novo lançamento no banco de dados usando a função do CRUD
    created_entry = entry_crud.create_with_owner(
        db=db, obj_in=entry_to_create, user_id=user_id
    )
    
    return created_entry