from pydantic import BaseModel

class ExtractedData(BaseModel):
  valor_total: float | None = None
  remetente: str | None = None
  destinatario: str | None = None

class BoundingBox(BaseModel):
  x_min: int
  y_min: int
  x_max: int
  y_max: int

class OCRItem(BaseModel):
  text: str
  confidence: float
  bounding_box: BoundingBox

# class OCRResponse(BaseModel):
#   data: list[OCRItem]

class OCRResponse(BaseModel):
  extracted_data: ExtractedData
  raw_ocr: list[OCRItem]
