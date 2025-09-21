# API Python Profissional com FastAPI, SQLAlchemy e MySQL

Stack: FastAPI (documentação automática Swagger/OpenAPI), SQLAlchemy 2.x (ORM), Alembic (migrações de banco de dados), Pydantic v2 (esquemas de dados), Uvicorn (servidor ASGI) e Poetry (gerenciamento de dependências).

## 1) Requisitos Mínimos
- Python 3.11+: Requisito essencial para o ambiente de execução.
- MySQL 8.0+: O banco de dados a ser usado. Certifique-se de que o servidor MySQL esteja instalado e rodando localmente.
- Poetry: Ferramenta para gerenciar as dependências do projeto. Você pode instalá-lo com pipx install poetry.

## 2) Instalação
Siga estes passos para configurar e executar o projeto na sua máquina local:

Instale o pipx

```
python -m pip install --user pipx
python -m pipx ensurepath
```

instale o poetry
```
python -m pip install --user poetry
```

Instale as dependências com Poetry
```
poetry install
```
Este comando lerá o arquivo pyproject.toml e instalará todas as dependências necessárias, incluindo as do grupo de desenvolvimento.

### 3) Configuração
Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto, seguindo o exemplo do arquivo .env.example

## 4) Execução
Inicialize a sessão do Poetry
```
poetry env use python
poetry env activate
```

rode o resultado do comando poetry env activate na sua linha de comando

Crie o banco de dados e aplique as migrações
Primeiro, certifique-se de que o banco de dados minha_api (ou o nome que você definiu no .env) já existe no seu servidor MySQL local. Você pode criá-lo com um cliente MySQL.
```
alembic upgrade head
```

Inicie o servidor da API
```
uvicorn app.main:app --reload
```
A API estará acessível em http://127.0.0.1:8000.

Documentação Interativa (Swagger UI): Acesse http://127.0.0.1:8000/docs para interagir com os endpoints da API.

Documentação Alternativa (ReDoc): Acesse http://127.0.0.1:8000/redoc.

## 5) Comandos Úteis
Para facilitar o desenvolvimento, você pode utilizar os comandos do Makefile:

- Rodar o projeto: uvicorn app.main:app --reload
- Atualizar o banco de dados: alembic upgrade head
- Criar migration: alembic revision -m "nome_migration" --autogenerate
- Testes: pytest -q

## 6) Configurar debug
- Execute o comando: poetry env info --executable
- Pegue o resultado desse comando e coloque no arquivo .vscode/launch.json em pythonPath