import os
from loguru import logger

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger.add(
    f"{LOG_DIR}/app.log",
    rotation="10 MB",
    retention="7 days",
    enqueue=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

# Opcional: mensagem de inicialização
logger.info("Logger configurado com sucesso.")
