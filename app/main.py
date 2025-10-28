from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
<<<<<<< HEAD
<<<<<<< HEAD
from app.api.routers import users, health, auth, images, entry_type, entry
from app.api.routers import auth, entry, images, receipts
=======
from app.api.routers import users, health, auth, images, entry_type, entry, category, goal, notification
>>>>>>> origin/main
=======
from app.api.routers import users, health, auth, images, receipts, entry_type, entry, category
>>>>>>> 7dc122e3ab86853868dc347cecc7855854553682

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

app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(images.router, prefix=settings.API_V1_STR)
app.include_router(entry_type.router, prefix=settings.API_V1_STR)
app.include_router(entry.router, prefix=settings.API_V1_STR)
<<<<<<< HEAD
<<<<<<< HEAD
app.include_router(receipts.router, prefix=settings.API_V1_STR)
=======
app.include_router(category.router, prefix=settings.API_V1_STR)
app.include_router(goal.router, prefix=settings.API_V1_STR)
app.include_router(notification.router, prefix=settings.API_V1_STR)
>>>>>>> origin/main
=======
app.include_router(category.router, prefix=settings.API_V1_STR)
app.include_router(receipts.router, prefix=settings.API_V1_STR)
>>>>>>> 7dc122e3ab86853868dc347cecc7855854553682
