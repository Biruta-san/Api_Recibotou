from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.entry import EntryOut
from app.api.services import receipt_service
from app.models.user import User
from app.api.deps import get_current_user, get_db
from app.utils.responses import success_response, error_response, ResponseModel

router = APIRouter(prefix="/receipts", tags=["receipts"])

@router.post(
  "/upload",
  response_model=ResponseModel[EntryOut],
  status_code=status.HTTP_201_CREATED,
  summary="Processa um recibo e cria um lançamento"
)
async def upload_and_process_receipt(
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user),
  file: UploadFile = File(...)
):
  """
  Recebe um arquivo de imagem de um recibo, o processa e cria
  um novo lançamento (entrada ou saída) para o usuário logado.
  """
  try:
    # Chamada ao serviço assíncrono
    created_entry = await receipt_service.process_receipt_image(
      db=db, user_id=current_user.id, file=file
    )
    return success_response(
      data=EntryOut.from_orm(created_entry).model_dump(mode="json"),
      message="Notificação atualizada com sucesso.",
      status_code=status.HTTP_201_CREATED
    )
  except ValueError as e:
    return error_response(
      error="Value error",
      message="Erro de valor: " + str(e),
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
  except Exception as e:
    return error_response(
      error="Error processing receipt",
      message="Erro ao processar a receita: " + str(e),
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
