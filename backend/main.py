"""Aplicação FastAPI - Sistema de Conversão All-in-One."""

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from api.routes import router
from config import FRONTEND_PATH, STATIC_PATH

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação."""
    logger.info("Iniciando aplicação")
    yield
    logger.info("Encerrando aplicação")


app = FastAPI(
    title="Converter All-in-One",
    description="Sistema de conversão de documentos entre MD, DOCX, HTML, ODT, PDF, RST, RTF, TEX, TXT",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Captura exceções não tratadas e retorna mensagem legível."""
    if isinstance(exc, HTTPException):
        raise exc
    logger.exception("Exceção não tratada: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


if STATIC_PATH.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")


@app.get("/")
async def root():
    """Retorna a interface web ou mensagem da API."""
    index_path = FRONTEND_PATH / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Converter All-in-One API", "docs": "/docs"}


@app.get("/health")
async def health_check() -> dict:
    """Health check para monitoramento."""
    return {"status": "ok", "service": "converter-all-in-one"}
