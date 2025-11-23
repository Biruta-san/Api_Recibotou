# app/db/session.py (Versão Completa e Corrigida)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.core.config import settings

# Dicionário de argumentos extras para a conexão (usado para o SSL)
connect_args = {}

# Verifica se a URL é da Aiven (ou outra nuvem que exija SSL)
# Isso permite que o código funcione tanto localmente quanto na nuvem
if "aivencloud.com" in settings.SQLALCHEMY_DATABASE_URI:
    # Caminho para o arquivo ca.pem na raiz do projeto
    ssl_ca_path = os.path.join(os.getcwd(), "ca.pem")
    
    # Verifica se o arquivo existe antes de tentar usar
    if os.path.exists(ssl_ca_path):
        connect_args = {
            "ssl": {
                "ca": ssl_ca_path
            }
        }
        print(f"🔒 Conexão SSL ativada usando: {ssl_ca_path}")
    else:
        print("⚠️ AVISO: Você está tentando conectar na nuvem, mas o arquivo 'ca.pem' não foi encontrado na raiz.")

# Cria a engine de conexão
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    pool_pre_ping=True,
    connect_args=connect_args # Passa os argumentos de SSL aqui
)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- A FUNÇÃO QUE ESTAVA FALTANDO ---
def get_db():
    """
    Dependência do FastAPI que fornece uma sessão do banco de dados
    por requisição e garante que ela seja fechada no final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()