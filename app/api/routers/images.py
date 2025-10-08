# app/api/routers/images.py (Versão Definitiva)

from fastapi import APIRouter, File, UploadFile, HTTPException
from app.api.services import ocr_service  # <-- CORREÇÃO AQUI
from app.schemas.ocr import OCRResponse

router = APIRouter(tags=["images"])

@router.post("/ocr", response_model=OCRResponse, summary="Extrai texto de uma imagem usando EasyOCR.")
async def perform_ocr(file: UploadFile = File(...)):
    """
    Recebe uma imagem (PNG, JPEG, etc.) e retorna um JSON com o texto extraído.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é uma imagem.")

    try:
        contents = await file.read()
        
        ocr_results = ocr_service.extract_text_from_image_content(contents)
        
        return {"data": ocr_results}

    except ValueError as e: 
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar a imagem: {str(e)}")