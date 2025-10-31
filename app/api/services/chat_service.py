# app/api/services/chat_service.py (VERSÃO COMPLETA E REFINADA)

from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
import google.generativeai as genai
import json
import re
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.crud.entry import entry as crud_entry
from app.models.entry import Entry
from app.api.services import ocr_service # Importa o serviço de OCR que já funciona

# Configura o cliente do Google Gemini com a chave de API do nosso .env
genai.configure(api_key=settings.GOOGLE_API_KEY)

# 1. PROMPT DE EXTRAÇÃO DE INTENÇÃO (Sua lógica, agora em Python)
PROMPT_EXTRACAO_INTENCAO = f"""
Analise a pergunta do usuário sobre finanças pessoais e retorne um JSON com a intenção principal e as entidades relevantes.

Intenções Possíveis:
- resumo_mensal: Usuário quer um resumo de receitas e despesas de um mês específico.
- resumo_anual: Usuário quer um resumo/análise de um ano específico.
- consulta_despesas: Usuário quer saber sobre despesas (geral ou por categoria) em um período.
- consulta_receitas: Usuário quer saber sobre receitas em um período.
- consulta_cofrinho: Usuário quer saber sobre o saldo ou movimentações dos cofrinhos. (Será implementado no futuro)
- pergunta_geral: A pergunta não se encaixa nas categorias acima ou é conhecimento geral sobre finanças.

Entidades a Extrair (se presentes na pergunta):
- mes: Número do mês (1-12). Se não mencionado, retorne null. Considere "este mês" como o mês atual.
- ano: Número do ano (ex: 2025). Se não mencionado, retorne null. Considere "este ano" ou "ano passado" relativo ao ano atual.
- categoria: Nome da categoria de despesa ou receita mencionada (ex: "Alimentação", "Salário"). Se não mencionado, retorne null.
- nome_cofrinho: Nome do cofrinho mencionado. Se não mencionado, retorne null.

Ano Atual de Referência: {datetime.now().year}
Mês Atual de Referência: {datetime.now().month}

Formato da Resposta: JSON
Exemplo de Resposta para "quanto gastei com lazer em julho?":
{{
  "intencao": "consulta_despesas",
  "mes": 7,
  "ano": null,
  "categoria": "Lazer",
  "nome_cofrinho": null
}}

Exemplo de Resposta para "resumo do ano passado":
{{
  "intencao": "resumo_anual",
  "mes": null,
  "ano": {datetime.now().year - 1},
  "categoria": null,
  "nome_cofrinho": null
}}

Exemplo de Resposta para "dicas para economizar":
{{
  "intencao": "pergunta_geral",
  "mes": null,
  "ano": null,
  "categoria": null,
  "nome_cofrinho": null
}}

PERGUNTA DO USUÁRIO:
{{PERGUNTA_USUARIO}}

JSON RESULTADO:
"""

# 2. TRADUÇÃO DIRETA da sua função _extrairIntencaoComGemini
async def _extract_intent(question: str) -> dict | None:
    """Usa o Gemini para extrair a intenção e as entidades da pergunta do usuário."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt_completo = PROMPT_EXTRACAO_INTENCAO.replace("{{PERGUNTA_USUARIO}}", question)
    
    try:
        response = await model.generate_content_async(prompt_completo)
        texto_json = response.text
        json_limpo = re.sub(r'```json\s*|\s*```', '', texto_json, flags=re.DOTALL).strip()
        return json.loads(json_limpo)
    except Exception as e:
        print(f"Erro ao extrair intenção: {e}")
        return None

# --- Funções de Busca de Dados (Adaptação do seu código Dart) ---
async def _fetch_monthly_expense_data(db: Session, user_id: int, dt: datetime) -> List[Entry]:
    start_date = dt.replace(day=1)
    next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
    end_date = next_month - timedelta(days=1)
    
    # ID 2 = Despesa (conforme nossos testes)
    return crud_entry.get_many_by_owner(
        db, user_id=user_id, entry_type_id=2, start_date=start_date.date(), end_date=end_date.date()
    )

async def _fetch_monthly_income_data(db: Session, user_id: int, dt: datetime) -> List[Entry]:
    start_date = dt.replace(day=1)
    next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
    end_date = next_month - timedelta(days=1)
    
    # ID 1 = Receita (conforme nossos testes)
    return crud_entry.get_many_by_owner(
        db, user_id=user_id, entry_type_id=1, start_date=start_date.date(), end_date=end_date.date()
    )

# --- Funções de Construção de Prompt (TRADUÇÃO das suas _construirPrompt...) ---

def _build_monthly_summary_prompt(
    question: str, 
    receitas: List[Entry], 
    despesas: List[Entry], 
    dt: datetime
) -> str:
    # Formato de moeda simples para o backend
    currency_format = "R$ {:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    nome_do_mes = dt.strftime('%B')
    
    total_receitas = sum(entry.value for entry in receitas)
    total_despesas = sum(entry.value for entry in despesas)
    saldo_final = total_receitas - total_despesas
    
    prompt = f"""
    Sua tarefa é analisar os dados financeiros do usuário para o mês de {nome_do_mes} e responder à pergunta dele.
    Use APENAS os dados abaixo como fonte da verdade.
    
    --- DADOS FINANCEIROS ({nome_do_mes.capitalize()}) ---
    Total de Receitas Recebidas: {currency_format.format(total_receitas)}
    Total de Despesas Pagas: {currency_format.format(total_despesas)}
    Saldo do Mês: {currency_format.format(saldo_final)}
    
    --- PERGUNTA DO USUÁRIO ---
    {question}
    
    --- SUA RESPOSTA ---
    Com base nos dados acima, responda de forma amigável e em português do Brasil. Se o saldo for positivo, elogie. Se for negativo, dê uma dica construtiva e direta.
    """
    return prompt

def _build_expense_prompt(
    question: str, 
    despesas: List[Entry], 
    dt: datetime, 
    categoria: Optional[str] = None
) -> str:
    currency_format = "R$ {:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    nome_do_mes = dt.strftime('%B')
    
    despesas_filtradas = despesas
    titulo_dados = f"Despesas de {nome_do_mes}"

    if categoria:
        despesas_filtradas = [d for d in despesas if categoria.lower() in d.description.lower()]
        titulo_dados = f"Despesas de {nome_do_mes} na categoria '{categoria}'"

    prompt = f"Você é um assistente financeiro. Responda à pergunta do usuário APENAS com base nos dados abaixo.\n\n"
    prompt += f"--- DADOS FINANCEIROS ({titulo_dados}) ---\n"

    if not despesas_filtradas:
        prompt += f"Nenhuma despesa encontrada para este critério no mês de {nome_do_mes}.\n"
    else:
        prompt += "Formato: [Descrição]; [Valor]\n"
        for despesa in despesas_filtradas:
            prompt += f"{despesa.description}; {currency_format.format(despesa.value)}\n"

    prompt += f"\n--- PERGUNTA DO USUÁRIO ---\n{question}\n"
    prompt += "\n--- SUA RESPOSTA ---"

    return prompt


# TODO: Implementar as funções para resumo anual, receitas e cofrinhos.

# 3. ORQUESTRADOR PRINCIPAL (Adaptação da sua função _sendMessage)
async def ask_question(db: Session, user_id: int, question: str) -> str:
    """Orquestra todo o processo de resposta do chatbot."""
    intent_json = await _extract_intent(question)
    
    intent = "pergunta_geral"
    data_para_busca = datetime.now()
    categoria = None
    
    if intent_json:
        intent = intent_json.get("intencao", "pergunta_geral")
        mes_extraido = intent_json.get("mes")
        ano_extraido = intent_json.get("ano")
        categoria = intent_json.get("categoria")
        
        ano_para_busca = ano_extraido or datetime.now().year
        if mes_extraido:
            data_para_busca = datetime(ano_para_busca, mes_extraido, 1)
        elif ano_extraido:
            data_para_busca = datetime(ano_para_busca, 1, 1)
            
    # 2. Buscar dados e construir o prompt final
    
    if intent == "resumo_mensal":
        despesas = await _fetch_monthly_expense_data(db, user_id, data_para_busca)
        receitas = await _fetch_monthly_income_data(db, user_id, data_para_busca)
        
        # Chama a função que criamos acima
        prompt_final = _build_monthly_summary_prompt(question, receitas, despesas, data_para_busca)
        
    elif intent == "consulta_despesas":
        # TODO: Implementar a busca de despesas por categoria/mês e chamar um prompt específico
        # Por enquanto, vamos retornar uma resposta indicando que a lógica está aqui
        return "Entendi que você quer consultar despesas. Vamos implementar isso em seguida!"
        
    # ... TODO: Adicionar a lógica para as outras intenções ...

    else: # Pergunta geral
        prompt_final = f"Responda sempre em português do Brasil. A minha pergunta é: {question}"

    # 3. Gerar a resposta final com o Gemini
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = await model.generate_content_async(prompt_final)
    
    return response.text