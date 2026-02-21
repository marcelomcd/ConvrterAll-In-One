"""Serviço de conversão de documentos."""

import logging
import os
import tempfile
from pathlib import Path

from config import (
    CONTENT_TYPES,
    DEFAULT_PLACEHOLDER,
    MAX_FILE_SIZE_BYTES,
    OUTPUT_FORMATS,
)
from domain.models import ConvertRequest, ConvertResult
from converter.docx_merge import merge_with_template_to_buffer
from converter.pandoc_engine import PandocEngine
from converter.pdf_engine import convert_to_pdf_bytes

logger = logging.getLogger(__name__)


def _format_error(exc: Exception) -> str:
    """Formata erro de conversão com mensagem amigável."""
    return f"Erro na conversão: {exc}"


class ConversionError(Exception):
    """Erro na conversão ou validação de documento."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


class ConvertService:
    """Caso de uso: converter documento para outro formato."""

    def execute(self, request: ConvertRequest) -> ConvertResult:
        """
        Executa a conversão conforme a requisição.

        Args:
            request: Dados da requisição de conversão.

        Returns:
            Resultado com conteúdo, nome do arquivo e content-type.

        Raises:
            ConversionError: Quando a conversão falha.
        """
        output_format = request.output_format.lower().strip()
        self._validate_output_format(output_format)
        self._validate_file_sizes(request)

        if self._should_use_template(request, output_format):
            return self._convert_with_template(request, output_format)
        return self._convert_direct(request, output_format)

    def _validate_output_format(self, output_format: str) -> None:
        if output_format not in OUTPUT_FORMATS:
            raise ConversionError(
                f"Formato inválido. Use: {', '.join(sorted(OUTPUT_FORMATS))}"
            )

    def _validate_file_sizes(self, request: ConvertRequest) -> None:
        limit_mb = MAX_FILE_SIZE_BYTES // (1024 * 1024)
        if len(request.source_content) > MAX_FILE_SIZE_BYTES:
            raise ConversionError(
                f"Arquivo de origem muito grande. Limite: {limit_mb}MB",
                status_code=413,
            )
        if request.template_content and len(request.template_content) > MAX_FILE_SIZE_BYTES:
            raise ConversionError(
                f"Template muito grande. Limite: {limit_mb}MB",
                status_code=413,
            )

    def _should_use_template(
        self, request: ConvertRequest, output_format: str
    ) -> bool:
        return (
            output_format == "docx"
            and request.template_content is not None
            and len(request.template_content) > 0
        )

    def _convert_with_template(
        self, request: ConvertRequest, output_format: str
    ) -> ConvertResult:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            source_path = tmppath / (request.source_filename or "source.md")
            source_path.write_bytes(request.source_content)

            template_path = tmppath / "template.docx"
            template_path.write_bytes(request.template_content)

            try:
                temp_docx = PandocEngine.convert_to_temp_docx(source_path)
            except Exception as exc:
                logger.exception("Erro ao converter para DOCX temporário")
                raise ConversionError(_format_error(exc)) from exc

            try:
                result_bytes = merge_with_template_to_buffer(
                    template_path=str(template_path),
                    content_path=temp_docx,
                    pattern=request.placeholder or DEFAULT_PLACEHOLDER,
                )
            except Exception as exc:
                logger.exception("Erro ao mesclar template DOCX")
                raise ConversionError(_format_error(exc)) from exc
            finally:
                if os.path.exists(temp_docx):
                    os.remove(temp_docx)

            filename = Path(request.source_filename or "output").stem + ".docx"
            return ConvertResult(
                content=result_bytes,
                filename=filename,
                content_type=CONTENT_TYPES["docx"],
            )

    def _convert_direct(
        self, request: ConvertRequest, output_format: str
    ) -> ConvertResult:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            source_path = tmppath / (request.source_filename or "source.md")
            source_path.write_bytes(request.source_content)

            ext = PandocEngine.get_output_extension(output_format)
            output_filename = Path(request.source_filename or "output").stem + ext
            output_path = tmppath / output_filename

            try:
                if output_format == "pdf":
                    result_bytes = convert_to_pdf_bytes(source_path)
                else:
                    PandocEngine.convert(
                        source_path=source_path,
                        output_format=output_format,
                        output_path=output_path,
                    )
                    if not output_path.exists():
                        raise ConversionError("Arquivo de saída não foi gerado")
                    result_bytes = output_path.read_bytes()
            except Exception as exc:
                logger.exception("Erro ao converter documento")
                raise ConversionError(_format_error(exc)) from exc

            content_type = CONTENT_TYPES.get(
                output_format, "application/octet-stream"
            )
            return ConvertResult(
                content=result_bytes,
                filename=output_filename,
                content_type=content_type,
            )
