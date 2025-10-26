from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """
    Formata um objeto datetime no formato 'dd/mm/yyyy hh:mm'.

    Exemplo:
        dt = datetime.now()
        format_datetime(dt) -> '25/10/2025 21:45'
    """
    return dt.strftime("%d/%m/%Y %H:%M")
