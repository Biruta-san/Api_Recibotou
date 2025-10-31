from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
# Importamos as constantes diretamente do FastAPI para não depender de um arquivo de utilitário
from fastapi import status as http_status 
from app.api.deps import get_db, get_current_active_user # <-- CORREÇÃO 1: Usar a dependência correta
from app.crud.entry_type import entry_type as crud_entry_type
from app.models.user import User
from app.schemas.entry_type import EntryTypeCreate, EntryTypeOut, EntryTypeUpdate
from app.utils.responses import success_response, error_response, ResponseModel
from app.utils.enum import TipoLancamento

# Para resolver o problema de importação do TipoLancamento, assumimos que ele é um Enum simples
# Se for uma classe maior, o erro persistirá até vermos o arquivo app/utils/enum.py

router = APIRouter(prefix="/entry_types", tags=["entry_types"])


"""
Cria um novo tipo de lançamento financeiro. (Não precisa de login, mas é boa prática proteger)
"""
@router.post("/", status_code=http_status.HTTP_201_CREATED, response_model=ResponseModel[EntryTypeOut])
def create_entry_type(
    entry_type_in: EntryTypeCreate, 
    db: Session = Depends(get_db),
    # Embora a criação de um tipo de lançamento possa ser para todos, é comum proteger esta rota
    current_user: User = Depends(get_current_active_user) 
):
    entry_type = crud_entry_type.create(db, entry_type_in)
    return success_response(
        data=EntryTypeOut.from_orm(entry_type).model_dump(),
        message="Tipo de lançamento criado com sucesso.",
        status_code=http_status.HTTP_201_CREATED
    )

"""
Atualiza os dados de um tipo de lançamento. (Protegido)
"""
@router.patch("/{entry_type_id}", response_model=ResponseModel[EntryTypeOut])
def update_entry_type(
    entry_type_id: int, 
    entry_type_in: EntryTypeUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- CORREÇÃO 1: Dependência correta
):
    obj = crud_entry_type.get(db, entry_type_id)

    if not obj:
        return error_response(
            error="Entry type not found",
            message="Tipo de lançamento não encontrado para atualização.",
            status_code=http_status.HTTP_404_NOT_FOUND
        )

    updated_entry_type = crud_entry_type.update(db, obj, entry_type_in)
    return success_response(
        data=EntryTypeOut.from_orm(updated_entry_type).model_dump(),
        message="Tipo de lançamento atualizado com sucesso."
    )

"""
Obtém os dados de um tipo de lançamento específico pelo ID. (Protegido)
"""
@router.get("/{entry_type_id}", response_model=ResponseModel[EntryTypeOut])
def read_entry_type(
    entry_type_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- CORREÇÃO 1: Dependência correta
):
    obj = crud_entry_type.get(db, entry_type_id)

    if not obj:
        return error_response(
            error="Entry type not found",
            message="Tipo de lançamento não encontrado.",
            status_code=http_status.HTTP_404_NOT_FOUND
        )

    return success_response(
        data=EntryTypeOut.from_orm(obj).model_dump(),
        message="Tipo de lançamento encontrado com sucesso."
    )

"""
Obtém os dados de todos os tipos de lançamento. (Protegido)
"""
@router.get("/", response_model=ResponseModel[list[EntryTypeOut]])
def read_entry_types(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- CORREÇÃO 1: Dependência correta
):
    obj = crud_entry_type.get_many(db)

    if not obj:
        return error_response(
            error="Entry types not found",
            message="Tipos de lançamento não encontrados.",
            status_code=http_status.HTTP_404_NOT_FOUND
        )

    # Use EntryTypeOut.from_orm(item) em vez de model_validate(item) se item for um objeto SQLAlchemy
    return success_response(
        data=[EntryTypeOut.from_orm(item).model_dump() for item in obj], 
        message="Tipos de lançamento encontrados com sucesso."
    )

"""
Remove um tipo de lançamento do sistema. (Protegido)
"""
@router.delete("/{entry_type_id}", status_code=http_status.HTTP_200_OK, response_model=ResponseModel[None])
# <-- CORREÇÃO 2: Renomear para o nome correto 'delete_entry_type'
def delete_entry_type(
    entry_type_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <-- CORREÇÃO 1: Dependência correta
):
    # Lógica de proteção contra exclusão de tipos base
    if entry_type_id in [TipoLancamento.DESPESA, TipoLancamento.RECEITA]:
        return error_response(
            error="Entry Type protected",
            message="Tipo de lançamento protegido e não pode ser excluído.",
            status_code=http_status.HTTP_403_FORBIDDEN
        )

    obj = crud_entry_type.remove(db, entry_type_id)

    # Se o objeto não foi encontrado para remoção, retorna erro
    if not obj:
        return error_response(
            error="Entry Type not found",
            message="Tipo de lançamento não encontrado para exclusão.",
            status_code=http_status.HTTP_404_NOT_FOUND
        )

    return success_response(
        message="Tipo de Lançamento removido com sucesso."
    )