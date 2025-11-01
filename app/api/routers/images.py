from fastapi import APIRouter, File, UploadFile, status
from app.api.services import ocr_service
from app.schemas.ocr import OCRResponse
from app.utils.responses import success_response, error_response, ResponseModel

router = APIRouter(tags=["images"])

@router.post("/ocr", response_model=ResponseModel[OCRResponse], summary="Extrai texto de uma imagem usando EasyOCR.")
async def perform_ocr(file: UploadFile = File(...)):
  """
  Recebe uma imagem (PNG, JPEG, etc.) e retorna um JSON com o texto extraído.
  """
  if not file.content_type.startswith("image/"):
    return error_response(
      error="Invalid file type",
      message="O Conteúdo enviado não é uma imagem válida.",
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

  try:
    contents = await file.read()

    ocr_results = ocr_service.extract_text_from_image_content(contents)

    return success_response(
      data={"data": ocr_results},
      message="Categoria criada com sucesso.",
      status_code=status.HTTP_201_CREATED
    )

  except ValueError as e:
    return error_response(
      error="Value error",
      message="Erro de valor ao processar a imagem: " + str(e),
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
  except RuntimeError as e:
    return error_response(
      error="Runtime error",
      message="Erro em tempo de execução ao processar a imagem: " + str(e),
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
