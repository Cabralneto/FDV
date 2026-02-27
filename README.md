# FDV - Sistema Técnico de Documentos de Engenharia

Plataforma interna para ingestão contínua de PDFs de engenharia, com versionamento por revisão, extração automática de dados técnicos e busca textual.

## Visão da arquitetura

- **Backend**: FastAPI (Python)
- **Banco**: PostgreSQL
- **Extração PDF**: `pdfplumber` ou `PyMuPDF`
- **Busca**: PostgreSQL Full Text Search (`tsvector` + GIN)
- **Frontend**: Next.js (React)

Pipeline operacional:

`Upload -> Extração -> Indexação -> Estruturação -> Armazenamento`

## Estrutura do repositório

- `backend/`: API, regras de negócio e persistência
- `backend/sql/`: DDL relacional completo
- `frontend/`: base inicial do painel e consultas
- `docs/`: arquitetura e exemplos de queries

## Como executar (local)

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3) Banco

Aplicar o script:

```bash
psql -U <usuario> -d <database> -f backend/sql/schema.sql
```

## Próximos passos recomendados

1. Adicionar autenticação (SSO interno ou JWT)
2. Processamento assíncrono (Celery/RQ)
3. OCR para PDFs escaneados
4. Controle de permissões por área e disciplina
