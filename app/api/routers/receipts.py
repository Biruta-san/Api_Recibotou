from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.entry import EntryOut
from app.api.services import receipt_service
from app.models.user import User
from app.api.deps import get_current_user, get_db

router = APIRouter(prefix="/receipts", tags=["Receipts"])

@router.post(
    "/upload",
    response_model=EntryOut,
    status_code=status.HTTP_201_CREATED,
    summary="Processa um recibo e cria um lançamento"
)
async def upload_and_process_receipt(
    *,
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
    return EntryOut.from_orm(created_entry)
  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
      detail=str(e),
    )
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Ocorreu um erro inesperado: {e}",
    )
