"""Motor de conversão para PDF via markdown-pdf (pip install)."""

import io
import tempfile
from pathlib import Path

from converter.pandoc_engine import PandocEngine
from markdown_pdf import MarkdownPdf, Section


def convert_to_pdf(
    source_path: str | Path,
    output_path: str | Path,
    input_format: str | None = None,
) -> str:
    """
    Converte o arquivo para PDF usando markdown-pdf (100% pip).

    Fluxo: input -> Pandoc -> Markdown -> markdown-pdf -> PDF
    """
    source_path = Path(source_path)
    output_path = Path(output_path)

    if input_format is None:
        input_format = PandocEngine.detect_input_format(str(source_path))

    md_content = _to_markdown(source_path, input_format)
    _markdown_to_pdf(md_content, output_path)
    return str(output_path)


def convert_to_pdf_bytes(
    source_path: str | Path,
    input_format: str | None = None,
) -> bytes:
    """Converte para PDF e retorna bytes."""
    source_path = Path(source_path)
    if input_format is None:
        input_format = PandocEngine.detect_input_format(str(source_path))

    md_content = _to_markdown(source_path, input_format)
    buffer = io.BytesIO()
    pdf = MarkdownPdf(toc_level=2, optimize=True)
    pdf.add_section(Section(md_content))
    pdf.save_bytes(buffer)
    return buffer.getvalue()


def _to_markdown(source_path: Path, input_format: str) -> str:
    """Converte qualquer formato para Markdown via Pandoc."""
    if input_format == "markdown":
        return source_path.read_text(encoding="utf-8")
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".md",
        delete=False,
        encoding="utf-8",
    ) as tmp:
        tmp_path = tmp.name
    try:
        PandocEngine.convert(
            source_path=source_path,
            output_format="markdown",
            output_path=tmp_path,
            input_format=input_format,
        )
        return Path(tmp_path).read_text(encoding="utf-8")
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def _markdown_to_pdf(md_content: str, output_path: Path) -> None:
    """Converte Markdown para PDF usando markdown-pdf."""
    pdf = MarkdownPdf(toc_level=2, optimize=True)
    pdf.add_section(Section(md_content))
    pdf.save(str(output_path))
