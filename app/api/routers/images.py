import easyocr
from pydantic import BaseModel
from fastapi import APIRouter, File, UploadFile, HTTPException
import numpy as np
import cv2

router = APIRouter(tags=["images"])

reader = easyocr.Reader(['pt'])

class BoundingBox(BaseModel):
    x_min: int
    y_min: int
    x_max: int
    y_max: int

class OCRItem(BaseModel):
    text: str
    confidence: float
    bounding_box: BoundingBox

class OCRResponse(BaseModel):
    data: list[OCRItem]

@router.post("/ocr", response_model=OCRResponse, summary="Extrai texto de uma imagem usando EasyOCR.")
async def perform_ocr(file: UploadFile = File(...)):
    """
    Recebe uma imagem (PNG, JPEG, etc.) e retorna um JSON com o texto extraído.
    """
    # Verifica se o arquivo é uma imagem
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="O arquivo enviado não é uma imagem."
        )

    try:
        # Lê o conteúdo da imagem
        contents = await file.read()
        
        # Converte os bytes da imagem para um array numpy, necessário para o EasyOCR
        image_as_array = np.frombuffer(contents, np.uint8)

        image_np = cv2.imdecode(image_as_array, cv2.IMREAD_COLOR)

        if image_np is None:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível decodificar a imagem. O arquivo pode estar corrompido ou em um formato inválido."
            )

        # Chama o EasyOCR para processar a imagem
        results = reader.readtext(image_np)

        # Formata os resultados em um formato de lista JSON
        formatted_results = []
        for (bbox, text, confidence) in results:
            x_min, y_min = [int(i) for i in bbox[0]]
            x_max, y_max = [int(i) for i in bbox[2]]
            
            formatted_results.append({
                "text": text,
                "confidence": confidence,
                "bounding_box": {
                    "x_min": x_min,
                    "y_min": y_min,
                    "x_max": x_max,
                    "y_max": y_max
                }
            })
        
        return {"data": formatted_results}

    except Exception as e:
        # Lidar com erros de processamento da imagem
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar a imagem: {str(e)}"
        )