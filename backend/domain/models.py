"""Modelos de domínio e DTOs."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConvertRequest:
    """Requisição de conversão."""

    source_content: bytes
    source_filename: str
    output_format: str
    template_content: bytes | None = None
    placeholder: str = "{{CONTEUDO}}"


@dataclass(frozen=True)
class ConvertResult:
    """Resultado da conversão."""

    content: bytes
    filename: str
    content_type: str
