# app/api/services/ocr_service.py

import easyocr
import numpy as np
import cv2

# Inicializa o 'leitor' do EasyOCR uma única vez quando o módulo é importado.
# Isso é muito mais eficiente, pois evita recarregar o modelo de IA a cada chamada.
reader = easyocr.Reader(['pt'])

def extract_text_from_image_content(contents: bytes) -> list[dict]:
    """
    Recebe o conteúdo de uma imagem em bytes, processa com EasyOCR
    e retorna uma lista de dicionários com os resultados formatados.

    Args:
        contents (bytes): O conteúdo binário de um arquivo de imagem.

    Raises:
        ValueError: Se o conteúdo da imagem não puder ser decodificado.
        RuntimeError: Para outros erros inesperados durante o processamento do OCR.

    Returns:
        list[dict]: Uma lista de dicionários, cada um contendo o texto,
                    a confiança e a caixa delimitadora.
    """
    try:
        # Converte os bytes da imagem em um array numpy
        image_as_array = np.frombuffer(contents, np.uint8)
        # Decodifica o array em uma imagem que o OpenCV/EasyOCR pode ler
        image_np = cv2.imdecode(image_as_array, cv2.IMREAD_COLOR)

        if image_np is None:
            raise ValueError("Não foi possível decodificar a imagem. O arquivo pode estar corrompido ou em um formato inválido.")

        # Realiza a extração de texto na imagem
        results = reader.readtext(image_np)

        # Formata a saída do EasyOCR para o nosso schema padronizado
        formatted_results = []
        for (bbox, text, confidence) in results:
            # Extrai as coordenadas da caixa delimitadora
            x_min, y_min = [int(point) for point in bbox[0]]
            x_max, y_max = [int(point) for point in bbox[2]]

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
        # Encapsula a exceção original em um RuntimeError para não vazar detalhes
        # da implementação e permite que quem chamou a função trate o erro.
        raise RuntimeError(f"Erro interno no processamento do EasyOCR: {e}") from e