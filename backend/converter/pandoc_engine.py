"""Motor de conversão via Pandoc."""

import logging
import os
import tempfile
from pathlib import Path

import pypandoc

logger = logging.getLogger(__name__)
_pandoc_ensured = False


def ensure_pandoc() -> None:
    """
    Garante que o Pandoc está disponível.
    Se não estiver no PATH, tenta fazer o download automático.
    """
    global _pandoc_ensured
    if _pandoc_ensured:
        return
    try:
        pypandoc.get_pandoc_path()
        _pandoc_ensured = True
    except OSError:
        logger.info("Pandoc não encontrado. Iniciando download automático...")
        pypandoc.download_pandoc()
        _pandoc_ensured = True
        logger.info("Pandoc instalado com sucesso.")


# Mapeamento de extensões para formatos Pandoc
EXT_TO_PANDOC = {
    ".md": "markdown",
    ".markdown": "markdown",
    ".html": "html",
    ".htm": "html",
    ".rst": "rst",
    ".tex": "latex",
    ".txt": "plain",
    ".docx": "docx",
    ".odt": "odt",
}

PANDOC_TO_EXT = {
    "docx": ".docx",
    "html": ".html",
    "markdown": ".md",
    "md": ".md",
    "odt": ".odt",
    "pdf": ".pdf",
    "rst": ".rst",
    "rtf": ".rtf",
    "latex": ".tex",
    "tex": ".tex",
    "plain": ".txt",
    "txt": ".txt",
}

# Formatos de entrada e saída suportados
INPUT_FORMATS = {"markdown", "html", "rst", "latex", "plain", "docx", "odt"}
OUTPUT_FORMATS = {
    "docx", "html", "markdown", "md", "odt", "pdf", "rst", "rtf", "latex", "tex",
    "plain", "txt",
}
# Alias para formato Pandoc (API usa md/tex, Pandoc usa markdown/latex)
OUTPUT_FORMAT_ALIASES = {"md": "markdown", "tex": "latex", "txt": "plain"}


class PandocEngine:
    """Encapsula chamadas ao Pandoc para conversão de documentos."""

    @staticmethod
    def detect_input_format(filename: str) -> str:
        """Detecta o formato de entrada pela extensão do arquivo."""
        ext = Path(filename).suffix.lower()
        return EXT_TO_PANDOC.get(ext, "markdown")

    @staticmethod
    def get_output_extension(output_format: str) -> str:
        """Retorna a extensão do arquivo para o formato de saída."""
        return PANDOC_TO_EXT.get(output_format.lower(), ".bin")

    @staticmethod
    def convert(
        source_path: str | Path,
        output_format: str,
        output_path: str | Path | None = None,
        input_format: str | None = None,
        reference_doc: str | Path | None = None,
    ) -> str | bytes:
        """
        Converte o arquivo de origem para o formato de saída.

        Args:
            source_path: Caminho do arquivo de origem.
            output_format: Formato de saída (docx, html, md, odt, pdf, rst, rtf, tex, txt).
            output_path: Caminho do arquivo de saída. Se None, retorna bytes.
            input_format: Formato de entrada. Se None, detecta pela extensão.
            reference_doc: Caminho do DOCX de referência para estilos (só para saída docx).

        Returns:
            Caminho do arquivo gerado ou bytes se output_path for None.
        """
        ensure_pandoc()
        source_path = Path(source_path)
        output_format = output_format.lower()

        if output_format not in OUTPUT_FORMATS:
            raise ValueError(f"Formato de saída não suportado: {output_format}")

        pandoc_format = OUTPUT_FORMAT_ALIASES.get(output_format, output_format)

        if input_format is None:
            input_format = PandocEngine.detect_input_format(str(source_path))

        if input_format not in INPUT_FORMATS:
            raise ValueError(f"Formato de entrada não suportado: {input_format}")

        extra_args = []
        if pandoc_format == "docx" and reference_doc:
            extra_args = [f"--reference-doc={reference_doc}"]
        if pandoc_format == "pdf":
            raise ValueError("PDF deve usar pdf_engine")

        if output_path:
            output_path = Path(output_path)
            pypandoc.convert_file(
                str(source_path),
                pandoc_format,
                format=input_format,
                outputfile=str(output_path),
                extra_args=extra_args,
            )
            return str(output_path)

        return pypandoc.convert_file(
            str(source_path),
            pandoc_format,
            format=input_format,
            extra_args=extra_args,
        )

    @staticmethod
    def convert_to_temp_docx(
        source_path: str | Path,
        input_format: str | None = None,
    ) -> str:
        """
        Converte o arquivo para DOCX em um arquivo temporário.

        Usado como passo intermediário para merge com template.
        """
        ensure_pandoc()
        source_path = Path(source_path)
        if input_format is None:
            input_format = PandocEngine.detect_input_format(str(source_path))

        fd, temp_path = tempfile.mkstemp(suffix=".docx")
        os.close(fd)
        PandocEngine.convert(source_path, "docx", temp_path, input_format)
        return temp_path
