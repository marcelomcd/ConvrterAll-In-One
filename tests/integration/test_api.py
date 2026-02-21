"""Testes de integração da API."""

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestHealthCheck:
    """Testes do endpoint de health check."""

    def test_health_retorna_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "converter-all-in-one" in data["service"]

    def test_health_resposta_valida(self):
        response = client.get("/health")
        assert "status" in response.json()
        assert "service" in response.json()


class TestFormatsEndpoint:
    """Testes do endpoint de formatos."""

    def test_lista_formatos_retorna_200(self):
        response = client.get("/api/formats")
        assert response.status_code == 200

    def test_lista_formatos_tem_estrutura_esperada(self):
        response = client.get("/api/formats")
        data = response.json()
        assert "output_formats" in data
        assert "docx" in data["output_formats"]
        assert "html" in data["output_formats"]
        assert "from_md" in data
        assert "to_md" in data


class TestConvertEndpoint:
    """Testes do endpoint de conversão."""

    def test_convert_sem_arquivo_retorna_422(self):
        response = client.post(
            "/api/convert",
            data={"output_format": "docx"},
        )
        assert response.status_code == 422

    def test_convert_com_formato_invalido_retorna_400(self):
        response = client.post(
            "/api/convert",
            data={"output_format": "invalid"},
            files={"source_file": ("test.md", b"# Hello", "text/markdown")},
        )
        assert response.status_code == 400
        assert "Formato inválido" in response.json()["detail"]
