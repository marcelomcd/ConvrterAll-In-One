"""Configurações da aplicação."""

from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = Path(__file__).resolve().parent
FRONTEND_PATH = PROJECT_ROOT / "frontend"
STATIC_PATH = FRONTEND_PATH / "static"

# Limites
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
MAX_FILE_SIZE_MB = 10

# Formatos
OUTPUT_FORMATS = frozenset(
    ["docx", "html", "md", "odt", "pdf", "rst", "rtf", "tex", "txt"]
)
DEFAULT_PLACEHOLDER = "{{CONTEUDO}}"

# MIME types
CONTENT_TYPES = {
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "html": "text/html",
    "md": "text/markdown",
    "odt": "application/vnd.oasis.opendocument.text",
    "pdf": "application/pdf",
    "rst": "text/x-rst",
    "rtf": "application/rtf",
    "tex": "application/x-tex",
    "txt": "text/plain",
}
