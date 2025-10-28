from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.crud.category import category as crud_category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from app.utils.responses import success_response, error_response, ResponseModel
from app.utils.enum import Categoria # Assumindo que este import está correto

router = APIRouter(prefix="/categories", tags=["categories"])

"""
Cria uma nova categoria (Protegido por login)
"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[CategoryOut])
def create_category(
    category_in: CategoryCreate, 
    db: Session = Depends(get_db),
    # Adicionando dependência para garantir que só usuários logados possam criar categorias
    current_user: User = Depends(get_current_active_user)
):
    category = crud_category.create(db, category_in)
    return success_response(
        data=CategoryOut.from_orm(category).model_dump(),
        message="Categoria criada com sucesso.",
        status_code=status.HTTP_201_CREATED
    )

"""
Atualiza os dados de uma categoria (Protegido)
"""
@router.patch("/{category_id}", response_model=ResponseModel[CategoryOut])
def update_category(
    category_id: int, 
    category_in: CategoryUpdate, 
    db: Session = Depends(get_db), 
    # CORREÇÃO 1: Usar a dependência correta
    current_user: User = Depends(get_current_active_user)
):
    obj = crud_category.get(db, category_id)

    if not obj:
        return error_response(
            error="Category not found",
            message="Categoria não encontrada para atualização.",
            status_code=status.HTTP_404_NOT_FOUND
        )

    updated_category = crud_category.update(db, obj, category_in)
    return success_response(
        data=CategoryOut.from_orm(updated_category).model_dump(),
        message="Categoria atualizada com sucesso."
    )

"""
Obtém os dados de uma categoria especifica pelo Id (Protegido)
"""
@router.get("/{category_id}", response_model=ResponseModel[CategoryOut])
def read_category(
    category_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <--- CORREÇÃO: Fechando parêntese e adicionando dois pontos
):
    obj = crud_category.get(db, category_id)

    if not obj:
        return error_response(
            error="Category not found",
            message="Categoria não encontrada.",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return success_response(
        data=CategoryOut.from_orm(obj).model_dump(),
        message="Categoria encontrada com sucesso."
    )

"""
Obtém os dados de todas as categorias (Protegido)
"""
@router.get("/", response_model=ResponseModel[list[CategoryOut]])
def read_categories( # Renomeado para plural correto
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <--- CORREÇÃO: Fechando parêntese e adicionando dois pontos
):
    obj = crud_category.get_many(db)

    if not obj:
        return error_response(
            error="Category not found",
            message="Nenhuma categoria encontrada.",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return success_response(
        data=[CategoryOut.from_orm(item).model_dump() for item in obj], # Usando from_orm corretamente
        message="Categorias encontradas com sucesso."
    )

"""
Remove uma categoria do sistema (Protegido)
"""
@router.delete("/{category_id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[None])
def delete_category( # Renomeado para o nome correto
    category_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user) # <--- CORREÇÃO: Fechando parêntese e adicionando dois pontos
):
    # Lógica de proteção contra exclusão de categorias padrão
    if category_id in [Categoria.ALIMENTACAO, Categoria.CASA, Categoria.EDUCACAO,
                      Categoria.ENTRETENIMENTO, Categoria.OUTROS, Categoria.ROUPAS,
                      Categoria.SAUDE, Categoria.TRANSPORTE]:
        return error_response(
            error="Category protected",
            message="Categoria protegida e não pode ser excluída.",
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    obj = crud_category.remove(db, category_id)

    if not obj:
        return error_response(
            error="Category not found",
            message="Categoria não encontrada para exclusão.",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return success_response(
        message="Categoria removida com sucesso."
    )