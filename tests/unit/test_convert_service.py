"""Testes do serviço de conversão."""

import pytest

from domain.models import ConvertRequest
from services.convert_service import ConversionError, ConvertService


class TestConvertServiceValidation:
    """Testes de validação do ConvertService."""

    def test_rejeita_formato_invalido(self):
        service = ConvertService()
        request = ConvertRequest(
            source_content=b"# Test",
            source_filename="test.md",
            output_format="invalid_format",
        )
        with pytest.raises(ConversionError) as exc_info:
            service.execute(request)
        assert "Formato inválido" in str(exc_info.value)
        assert exc_info.value.status_code == 400

    def test_rejeita_arquivo_muito_grande(self):
        service = ConvertService()
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        request = ConvertRequest(
            source_content=large_content,
            source_filename="test.md",
            output_format="docx",
        )
        with pytest.raises(ConversionError) as exc_info:
            service.execute(request)
        assert "muito grande" in str(exc_info.value)
        assert exc_info.value.status_code == 413
