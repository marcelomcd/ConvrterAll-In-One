"""Configuração do pytest e fixtures."""

import sys
from pathlib import Path

# Adiciona o backend ao path para imports
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))
