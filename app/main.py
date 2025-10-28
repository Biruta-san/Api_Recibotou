from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import users, health, auth, images, entry_type, entry
from app.api.routers import auth, entry, images, receipts
from app.api.routers import category, goal, notification
from app.api.routers import users, health, auth, images, entry_type, entry, category, analysis, chat


app = FastAPI(
  title=settings.PROJECT_NAME,
  openapi_url=f"{settings.API_V1_STR}/openapi.json",
  docs_url="/docs", # Swagger UI
  redoc_url="/redoc", # ReDoc
)

from app.core.logger_config import logger

# Redireciona '/' para '/docs'
@app.get("/", include_in_schema=False)
async def root():
  return RedirectResponse(url="/docs")

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.BACKEND_CORS_ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(images.router, prefix=settings.API_V1_STR, tags=["Images"]) # <-- Usando o nome correto do router
app.include_router(entry_type.router, prefix=settings.API_V1_STR)
app.include_router(entry.router, prefix=settings.API_V1_STR)
app.include_router(category.router, prefix=settings.API_V1_STR) # <-- Assumindo que o router é 'category'
app.include_router(receipts.router, prefix=settings.API_V1_STR) # <-- Router dos recibos
app.include_router(analysis.router, prefix=settings.API_V1_STR, tags=["Analysis"]) # <-- Nosso novo router
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["Chatbot"]) # <-- Nosso novo router
