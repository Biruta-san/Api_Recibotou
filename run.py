import os
import uvicorn
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

if __name__ == "__main__":
    # Pega as variáveis de ambiente que definem o endereço da API
    # Use os nomes que você definiu no seu .env
    # Se não existirem, usa valores padrão.
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    app_url = os.getenv("APP_URL", f"http://localhost:{port}")

    # Imprime a mensagem customizada e amigável
    print("=" * 60)
    print(f"🚀 API Recibotou iniciando...")
    print(f"✅ Ambiente carregado com sucesso.")
    print(f"🔗 A aplicação estará disponível em: {app_url}")
    print(f"📚 Documentação (Swagger UI): {app_url}/docs")
    print(f"📚 Documentação (ReDoc): {app_url}/redoc")
    print("=" * 60)

    # Inicia o Uvicorn programaticamente
    uvicorn.run(
        "app.main:app",  # Caminho para sua instância do FastAPI
        host=host,
        port=port,
        log_level="info"
    )
