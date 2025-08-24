from fastapi.responses import JSONResponse
from fastapi import status
from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel

# Tipo genérico (T) que pode ser qualquer modelo
T = TypeVar("T")

class ResponseModel(GenericModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    message: Optional[str] = None

def success_response(data=None, message: str = "Success", status_code: int = status.HTTP_200_OK):
    return JSONResponse(
        status_code=status_code,
        content=ResponseModel(success=True, data=data, message=message).model_dump()
    )

def error_response(error: str, message: str = "Error", status_code: int = status.HTTP_400_BAD_REQUEST):
    return JSONResponse(
        status_code=status_code,
        content=ResponseModel(success=False, error=error, message=message).model_dump()
    )
