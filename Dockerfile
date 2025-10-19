# --- Estágio 1: Builder ---
FROM python:3.12-slim-bookworm AS builder

# Variáveis de ambiente
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos do projeto
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# AQUI ESTÁ A MÁGICA ✨
# Instala o Poetry, depois instala a versão CPU-only do PyTorch e suas dependências diretas.
# Em seguida, roda o poetry install, que vai pular o torch por já estar instalado.
# No final, limpamos o cache para economizar espaço.
# DEPOIS (com a correção)
RUN pip uninstall -y bcrypt py-bcrypt && \
    pip install poetry && \
    pip install --no-cache-dir torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu && \
    poetry install --only main --no-root && \
    rm -rf ${POETRY_CACHE_DIR}

# --- Estágio 2: Final ---
FROM python:3.12-slim-bookworm AS final

# Instala dependências de sistema para a execução
RUN apt-get update && apt-get install -y \
    libgl1 \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

# Cria usuário não-root
RUN addgroup --system app && adduser --system --ingroup app app
ENV HOME=/app
USER app

# Define o diretório de trabalho
WORKDIR /app

# Copia o ambiente virtual e o código da aplicação
COPY --from=builder --chown=app:app /app/.venv ./.venv
COPY --chown=app:app . .

# Expõe a porta
EXPOSE 8000

# Comando de inicialização
CMD ["/bin/sh", "-c", ". ./.venv/bin/activate && alembic upgrade head && python run.py"]
