# app/api/services/receipt_service.py (Versão Final Corrigida)

from sqlalchemy.orm import Session
from fastapi import UploadFile
from datetime import date
import re

# Importa os módulos
from app.api.services import ocr_service
from app.crud.entry import entry as crud_entry # <--- O nome correto é este aqui
from app.schemas.entry import EntryCreate
from app.models.entry import Entry 

async def process_receipt_image(db: Session, user_id: int, file: UploadFile) -> Entry:
    """
    Orquestra o processo de converter a imagem de um recibo em um lançamento no banco.
    """
    # 1. Lê a imagem e extrai o texto usando nosso serviço de OCR
    image_content = await file.read()
    ocr_results = ocr_service.extract_text_from_image_content(image_content)
    
    if not ocr_results:
        raise ValueError("O recibo está ilegível e nenhum texto pôde ser extraído.")

    full_text = " ".join([item['text'] for item in ocr_results])
    full_text_lower = full_text.lower()

    # 2. Analisa o texto para encontrar o valor (ESTRATÉGIA DE PRIORIDADE)
    
    number_pattern = r'(\d{1,3}(?:[., ]\d{3})*(?:[.,]\d{2})?)'
    match = None
    
    # Prioridade 1: Busca explícita por R$ ou RS
    match = re.search(r'(?:r\$|rs)\s*' + number_pattern, full_text_lower)

    # Prioridade 2: Se não achou R$, busca por palavras-chave "Valor" ou "Total"
    if not match:
        match = re.search(r'(?:valor|total|pagamento)[:\s]*' + number_pattern, full_text_lower)

    # Prioridade 3: Busca por formato estrito de moeda BR
    if not match:
        match = re.search(r'(\d{1,3}(?:\.\d{3})*,\d{2})', full_text_lower)

    if not match:
        raise ValueError("Não foi possível identificar um valor monetário no recibo.")
    
    # Limpeza do valor encontrado
    raw_value = match.group(1)
    clean_value = raw_value.replace('.', '').replace(' ', '')
    clean_value = clean_value.replace(',', '.')
    
    try:
        value = float(clean_value)
    except ValueError:
        raise ValueError(f"Erro ao converter o valor encontrado: {raw_value}")

    # Define se é entrada ou saída
    entry_type_id = 2 # Padrão: Saída/Despesa (ID 2)
    income_keywords = ['pix recebido', 'salário', 'depósito', 'crédito', 'recebimento']
    if any(keyword in full_text_lower for keyword in income_keywords):
        entry_type_id = 1 # É Entrada/Receita (ID 1)
        
    # 3. Monta o objeto de criação
    DEFAULT_CATEGORY_ID = 1 
    
    entry_to_create = EntryCreate(
        title="Lançamento via Recibo",
        entry_date=date.today(),
        description=f"Lançamento automático via recibo: {full_text[:100]}...",
        value=value,
        entry_type_id=entry_type_id,
        user_id=user_id,
        category_id=DEFAULT_CATEGORY_ID
    )

    # 4. Salva o novo lançamento no banco de dados
    # CORREÇÃO AQUI: Usando o nome correto 'crud_entry' que foi importado
    created_entry = crud_entry.create_with_owner(
        db=db, obj_in=entry_to_create, user_id=user_id
    )
    
    return created_entry