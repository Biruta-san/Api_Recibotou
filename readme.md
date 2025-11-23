# API Python Profissional com FastAPI, SQLAlchemy e MySQL

Stack: FastAPI (documentação automática Swagger/OpenAPI), SQLAlchemy 2.x (ORM), Alembic (migrações de banco de dados), Pydantic v2 (esquemas de dados), Uvicorn (servidor ASGI) e Poetry (gerenciamento de dependências).

## 1) Requisitos Mínimos
- **Python 3.12 ou 3.13**: Requisito essencial. (Verifique com `py --list`).
- **MySQL 8.0+**: O banco de dados a ser usado.
- **Poetry**: Gerenciador de dependências.
- **Docker**: (Opcional) Para rodar em containers.

---

## 2) Rodando Localmente (Windows) - Passo a Passo Seguro

Siga estes passos exatos para evitar erros de caminho ou versão no Windows.

### 2.1) Instalação e Ambiente

1. **Instale o Poetry** (usando o módulo do Python para evitar erros de PATH):
   ```powershell
   python -m pip install --user poetry

python -m poetry env use python

python -m poetry install --no-root

python -m poetry run alembic upgrade head

python -m poetry run uvicorn app.main:app --reload --port 8001

Acessando a API
Após iniciar o servidor:

Documentação Interativa (Swagger): http://127.0.0.1:8001/docs

Documentação Alternativa (ReDoc): http://127.0.0.1:8001/redoc