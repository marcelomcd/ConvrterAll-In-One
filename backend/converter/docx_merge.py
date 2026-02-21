"""Merge de DOCX com template base."""

from pathlib import Path

from docx_merge import merge_docx


def merge_with_template(
    template_path: str | Path,
    content_path: str | Path,
    output_path: str | Path,
    pattern: str = "{{CONTEUDO}}",
) -> str:
    """
    Insere o conteúdo do content_path no template_path, substituindo o placeholder.

    Preserva capa, cabeçalhos, rodapés e layout do documento base.

    Args:
        template_path: Caminho do DOCX base (com placeholder).
        content_path: Caminho do DOCX com conteúdo a inserir.
        output_path: Caminho do arquivo de saída.
        pattern: String placeholder no template (ex: {{CONTEUDO}}).

    Returns:
        Caminho do arquivo gerado.
    """
    merge_docx(
        source_path=str(template_path),
        content_path=str(content_path),
        output_path=str(output_path),
        pattern=pattern,
    )
    return str(output_path)


def merge_with_template_to_buffer(
    template_path: str | Path,
    content_path: str | Path,
    pattern: str = "{{CONTEUDO}}",
) -> bytes:
    """
    Faz o merge e retorna os bytes do documento.

    Útil para streaming via API.
    """
    buffer = merge_docx(
        source_path=str(template_path),
        content_path=str(content_path),
        output_path=None,
        pattern=pattern,
    )
    return buffer.getvalue()
