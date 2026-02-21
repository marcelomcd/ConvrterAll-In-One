"""Injeção de dependências da API."""

from services.convert_service import ConvertService


def get_convert_service() -> ConvertService:
    """Retorna instância do serviço de conversão."""
    return ConvertService()
