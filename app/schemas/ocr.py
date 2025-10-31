from pydantic import BaseModel

# Define a estrutura da caixa delimitadora de cada texto detectado
class BoundingBox(BaseModel):
    x_min: int
    y_min: int
    x_max: int
    y_max: int

# Define a estrutura de cada item de texto que o OCR encontra
class OCRItem(BaseModel):
    text: str
    confidence: float
    bounding_box: BoundingBox

# Define a estrutura final da resposta da API de OCR
class OCRResponse(BaseModel):
    data: list[OCRItem]
