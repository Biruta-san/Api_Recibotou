from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health", summary="Healthcheck")
async def health():
  return {"status": "ok"}