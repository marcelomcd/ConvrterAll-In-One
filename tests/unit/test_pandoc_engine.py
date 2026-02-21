"""Testes do motor Pandoc."""

import pytest

from converter.pandoc_engine import PandocEngine


class TestDetectInputFormat:
    """Testes para detecção de formato de entrada."""

    def test_detecta_markdown_por_extensao_md(self):
        assert PandocEngine.detect_input_format("doc.md") == "markdown"

    def test_detecta_markdown_por_extensao_markdown(self):
        assert PandocEngine.detect_input_format("doc.markdown") == "markdown"

    def test_detecta_html(self):
        assert PandocEngine.detect_input_format("page.html") == "html"

    def test_detecta_rst(self):
        assert PandocEngine.detect_input_format("readme.rst") == "rst"

    def test_detecta_latex(self):
        assert PandocEngine.detect_input_format("doc.tex") == "latex"

    def test_detecta_plain_text(self):
        assert PandocEngine.detect_input_format("readme.txt") == "plain"

    def test_detecta_docx(self):
        assert PandocEngine.detect_input_format("documento.docx") == "docx"

    def test_default_para_extensao_desconhecida(self):
        assert PandocEngine.detect_input_format("file.xyz") == "markdown"


class TestGetOutputExtension:
    """Testes para extensão de saída."""

    def test_extensao_docx(self):
        assert PandocEngine.get_output_extension("docx") == ".docx"

    def test_extensao_html(self):
        assert PandocEngine.get_output_extension("html") == ".html"

    def test_extensao_pdf(self):
        assert PandocEngine.get_output_extension("pdf") == ".pdf"

    def test_extensao_markdown(self):
        assert PandocEngine.get_output_extension("md") == ".md"

    def test_extensao_case_insensitive(self):
        assert PandocEngine.get_output_extension("DOCX") == ".docx"
