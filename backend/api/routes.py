"""Endpoints de conversão."""

import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from config import DEFAULT_PLACEHOLDER, OUTPUT_FORMATS
from domain.models import ConvertRequest
from services.convert_service import ConversionError, ConvertService

router = APIRouter(prefix="/api", tags=["convert"])
logger = logging.getLogger(__name__)


@router.post("/convert")
async def convert(
    source_file: UploadFile = File(...),
    output_format: str = Form(...),
    template_file: UploadFile | None = File(default=None),
    placeholder: str = Form(default=DEFAULT_PLACEHOLDER),
) -> Response:
    """
    Converte o arquivo de origem para o formato especificado.

    - source_file: Arquivo de origem (obrigatório)
    - output_format: docx, html, md, odt, pdf, rst, rtf, tex, txt
    - template_file: Arquivo DOCX base (opcional, só para saída DOCX)
    - placeholder: Placeholder no template (default: {{CONTEUDO}})
    """
    template_content = None
    if template_file and template_file.filename:
        template_content = await template_file.read()

    content = await source_file.read()
    request = ConvertRequest(
        source_content=content,
        source_filename=source_file.filename or "source.md",
        output_format=output_format,
        template_content=template_content,
        placeholder=placeholder or DEFAULT_PLACEHOLDER,
    )

    try:
        result = ConvertService().execute(request)
        return Response(
            content=result.content,
            media_type=result.content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{result.filename}"'
            },
        )
    except Exception as exc:
        if isinstance(exc, ConversionError):
            status = getattr(exc, "status_code", 400)
            detail = str(exc)
            logger.warning("Erro de conversão: %s", detail)
        else:
            status = 500
            detail = str(exc)
            logger.exception("Erro inesperado na conversão: %s", exc)
        raise HTTPException(status_code=status, detail=detail) from exc


@router.get("/formats")
async def list_formats() -> dict:
    """Lista os formatos de conversão suportados."""
    return {
        "from_md": ["docx", "html", "md", "odt", "pdf", "rst", "rtf", "tex", "txt"],
        "to_md": ["html", "md", "rst", "tex", "txt"],
        "output_formats": sorted(OUTPUT_FORMATS),
    }
