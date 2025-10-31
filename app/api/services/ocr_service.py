# api/services/ocr_service.py

import easyocr
import numpy as np
import cv2
from fastapi import HTTPException

# Inicializa o reader uma única vez quando o módulo é carregado.
# Isso é mais eficiente do que inicializá-lo a cada chamada.
reader = easyocr.Reader(['pt'])

def extract_text_from_image_content(contents: bytes) -> list[dict]:
    """
    Recebe o conteúdo de uma imagem em bytes, processa com EasyOCR
    e retorna uma lista de dicionários com os resultados formatados.
    Esta é a lógica central que será reutilizada.
    """
    try:
        image_as_array = np.frombuffer(contents, np.uint8)
        image_np = cv2.imdecode(image_as_array, cv2.IMREAD_COLOR)

        if image_np is None:
            raise ValueError("Não foi possível decodificar a imagem. O arquivo pode estar corrompido ou em um formato inválido.")

        results = reader.readtext(image_np)

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
        
        return formatted_results

    except Exception as e:
        # Re-lança a exceção para que o chamador possa tratá-la
        # Adiciona um pouco mais de contexto ao erro.
        raise RuntimeError(f"Erro interno no processamento do EasyOCR: {e}") from e