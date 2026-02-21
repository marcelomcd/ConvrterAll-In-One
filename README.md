# Converter All-in-One

Sistema web para conversão de documentos entre múltiplos formatos (MD, DOCX, HTML, ODT, PDF, RST, RTF, TEX, TXT), com suporte a arquivo base DOCX para inserir o conteúdo convertido em templates preservando capa, cabeçalhos e rodapés.

## Arquitetura

O projeto segue princípios de Clean Code e arquitetura em camadas:

- **domain/**: Modelos e DTOs (ConvertRequest, ConvertResult)
- **services/**: Casos de uso (ConvertService)
- **converter/**: Infraestrutura (PandocEngine, docx_merge)
- **api/**: Controllers e endpoints FastAPI

## Formatos Suportados

### De Markdown (e outros)
- MD → DOCX, HTML, MD, ODT, PDF, RST, RTF, TEX, TXT

### Para Markdown
- HTML, MD, RST, TEX, TXT → MD

## Requisitos

- **Python 3.11+**
- **Pandoc** — incluído via `pypandoc-binary`
- **PDF** — incluído via `markdown-pdf` (100% pip, sem LaTeX ou wkhtmltopdf)

## Instalação

```bash
cd backend
pip install -r requirements.txt
```

**Nota para Windows:** Se a instalação do `lxml` falhar, tente primeiro `pip install lxml --only-binary :all:` e depois `pip install docx-merge-xml --no-deps`.

## Executar

### Opção 1: Script batch (Windows)

```batch
start.bat
```

### Opção 2: Linha de comando

```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Acesse: http://localhost:8000

## Testes

```bash
# Instalar dependências de desenvolvimento
pip install -r backend/requirements-dev.txt

# Executar todos os testes
python -m pytest tests/ -v

# Executar com cobertura
python -m pytest tests/ -v --cov=backend --cov-report=term-missing
```

## Uso do Template DOCX

Para converter conteúdo **dentro** de um documento Word existente:

1. Abra o arquivo DOCX base no Word
2. Insira o placeholder `{{CONTEUDO}}` no local desejado
3. Salve o documento
4. Na interface web, selecione o arquivo de origem e o arquivo base DOCX
5. Escolha "DOCX" como formato de saída e converta

## Estrutura do Projeto

```
ConvrterAll-In-One/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configurações
│   ├── domain/
│   │   └── models.py        # DTOs
│   ├── services/
│   │   └── convert_service.py
│   ├── converter/           # Infraestrutura
│   │   ├── pandoc_engine.py
│   │   └── docx_merge.py
│   ├── api/
│   │   ├── routes.py
│   │   └── dependencies.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   └── static/
│       ├── style.css
│       └── app.js
├── tests/
│   ├── unit/
│   └── integration/
├── start.bat                # Iniciar interface (Windows)
├── pyproject.toml           # Black, Ruff, Pytest
└── README.md
```

## API

### GET /health
Health check para monitoramento.

### POST /api/convert
- `source_file` (arquivo): arquivo de origem
- `output_format` (form): docx, html, md, odt, pdf, rst, rtf, tex, txt
- `template_file` (arquivo, opcional): DOCX base
- `placeholder` (form, opcional): placeholder no template (padrão: `{{CONTEUDO}}`)

### GET /api/formats
Lista os formatos suportados.

## Limites

- Tamanho máximo de upload: 10MB por arquivo

## Licença

MIT
