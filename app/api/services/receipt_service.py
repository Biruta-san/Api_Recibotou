# app/api/services/receipt_service.py (Versão Simplificada e Corrigida)

from sqlalchemy.orm import Session
from fastapi import UploadFile
from datetime import date
import re

# Importa os módulos
from app.api.services import ocr_service
from app.crud.entry import entry as crud_entry # Nome correto da importação
from app.schemas.entry import EntryCreate
from app.models.entry import Entry 

async def process_receipt_image(db: Session, user_id: int, user_name: str, file: UploadFile) -> Entry:
    """
    Orquestra o processo de converter a imagem de um recibo em um lançamento.
    """
    # 1. Lê a imagem e extrai o texto usando nosso serviço de OCR
    image_content = await file.read()
    ocr_results = ocr_service.extract_text_from_image_content(image_content)
    
    if not ocr_results:
        raise ValueError("O recibo está ilegível e nenhum texto pôde ser extraído.")

    # Junta tudo em uma linha só para facilitar a busca
    full_text = " ".join([item['text'] for item in ocr_results])
    full_text_lower = full_text.lower()

    # 2. Extração de Valor (A lógica de Prioridade que funcionou bem)
    number_pattern = r'(\d{1,3}(?:[., ]\d{3})*(?:[.,]\d{2})?)'
    match = re.search(r'(?:r\$|rs)\s*' + number_pattern, full_text_lower)
    
    if not match:
        match = re.search(r'(?:valor|total|pagamento)[:\s]*' + number_pattern, full_text_lower)
    if not match:
        match = re.search(r'(\d{1,3}(?:\.\d{3})*,\d{2})', full_text_lower)

    if not match:
        raise ValueError("Não foi possível identificar um valor monetário no recibo.")
    
    raw_value = match.group(1)
    clean_value = raw_value.replace('.', '').replace(' ', '').replace(',', '.')
    
    try:
        value = float(clean_value)
    except ValueError:
        raise ValueError(f"Erro ao converter o valor encontrado: {raw_value}")

    # 3. Lógica de Tipo (Simplificada: Nome do Usuário + Contexto)
    
    # IDs (Baseado nos seus testes: 1=Receita, 2=Despesa)
    ID_RECEITA = 1
    ID_DESPESA = 2
    
    entry_type_id = ID_DESPESA # Padrão: Assumimos que é Despesa (mais comum)

    # Prepara o primeiro nome do usuário para busca (mais seguro que nome completo por causa de erros de OCR)
    # Ex: "Davi Marques" -> busca apenas por "davi"
    first_name = user_name.lower().split()[0] if user_name else ""

    if first_name and first_name in full_text_lower:
        # Se achou o nome, vamos ver o que tem perto dele
        
        # Regex: Procura por "para", "destino" ou "favorecido" seguido de texto até encontrar o nome do usuário
        # Ex: "Para: Fulano de Tal Davi" -> Receita
        if re.search(r'(?:para|destino|favorecido|destinat[áa]rio).*?' + re.escape(first_name), full_text_lower):
            entry_type_id = ID_RECEITA
            
        # Regex: Procura por "de", "origem" ou "pagador" seguido de texto até encontrar o nome do usuário
        # Ex: "De: Davi Marques" -> Despesa
        elif re.search(r'(?:de:|origem|pagador).*?' + re.escape(first_name), full_text_lower):
            entry_type_id = ID_DESPESA
            
    else:
        # Se NÃO achou o nome do usuário (ou não conseguiu ler), vai pelas palavras-chave genéricas
        income_keywords = ['recebido', 'depósito', 'crédito', 'recebimento', 'entrada']
        if any(keyword in full_text_lower for keyword in income_keywords):
            entry_type_id = ID_RECEITA

    # 4. Montar e Salvar
    # Categoria 8 = Outros (conforme você configurou)
    DEFAULT_CATEGORY_ID = 8 
    
    entry_to_create = EntryCreate(
        title="Lançamento via Recibo",
        entry_date=date.today(),
        description=f"Lançamento automático via recibo: {full_text[:100]}...",
        value=value,
        entry_type_id=entry_type_id,
        user_id=user_id,
        category_id=DEFAULT_CATEGORY_ID
    )

    created_entry = crud_entry.create_with_owner(
        db=db, obj_in=entry_to_create, user_id=user_id
    )
    
    return created_entry