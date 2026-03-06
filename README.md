# Portal da Obra

Plataforma web para acompanhamento de obra industrial com ingestão de dados **somente leitura** a partir do SharePoint, consolidação em base própria, API REST e dashboards web.

> ⚠️ Regra crítica: o sistema **não pode** excluir, alterar, renomear, mover, sobrescrever ou gravar qualquer arquivo na origem (SharePoint). Toda persistência ocorre somente no PostgreSQL do Portal da Obra.

---

## 1) Visão geral da arquitetura

- **Frontend:** Next.js + React + TypeScript + Tailwind CSS.
- **Backend/API:** FastAPI (Python) + SQLAlchemy.
- **Banco:** PostgreSQL.
- **Ingestão:** pipeline Python com adapter SharePoint read-only + processamento incremental.
- **Agendamento:** APScheduler (execuções automáticas).
- **Containerização:** Docker + Docker Compose.

### Fluxo alto nível
1. Backend consulta arquivos da origem via adapter SharePoint read-only.
2. Detecta novos/alterados por hash/caminho/data.
3. Persiste dados normalizados em tabelas internas do PostgreSQL.
4. Frontend consulta endpoints da API para dashboards e telas operacionais.

---

## 2) Estrutura do projeto

```text
.
├── backend
│   ├── app
│   │   ├── api/v1
│   │   ├── core
│   │   ├── db
│   │   ├── ingestion
│   │   ├── models
│   │   ├── schemas
│   │   ├── services
│   │   └── workers
│   ├── alembic
│   ├── requirements.txt
│   └── scripts_seed.py
├── frontend
│   ├── src
│   │   ├── app
│   │   ├── components
│   │   └── lib
│   └── package.json
├── scripts
│   └── bootstrap.sh
├── docker-compose.yml
├── .env.example
├── backend/.env.example
└── frontend/.env.example
```

---

## 3) Pré-requisitos

### Opção A — Rodar com Docker (recomendado)
- Docker 24+
- Docker Compose plugin

### Opção B — Rodar sem Docker
- Python 3.11+
- Node.js 20+
- npm 10+
- PostgreSQL 16+

---

## 4) Variáveis de ambiente

Use os exemplos dedicados por camada:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

> O arquivo de raiz `.env.example` pode ser usado como referência consolidada, mas a execução local usa `backend/.env` e `frontend/.env.local`.

### Variáveis principais

| Variável | Onde usada | Exemplo | Descrição |
|---|---|---|---|
| `DATABASE_URL` | Backend | `postgresql+psycopg2://portal:portal@localhost:5432/portal_obra` | String de conexão do banco |
| `SECRET_KEY` | Backend | `super-secret` | Chave para token JWT |
| `SCHEDULER_ENABLED` | Backend | `true` | Liga/desliga execução automática de ingestão |
| `SCHEDULER_INTERVAL_MINUTES` | Backend | `15` | Intervalo do job de ingestão |
| `SHAREPOINT_MODE` | Backend | `mock` | Modo de integração (mock/futuro real) |
| `NEXT_PUBLIC_API_URL` | Frontend | `http://localhost:8000/api/v1` | URL pública da API consumida pelo frontend |

> Dica: em desenvolvimento local sem Docker, garanta que `DATABASE_URL` aponte para `localhost`. Em Docker Compose, a conexão interna usa host `postgres`.

---

## 5) Ordem correta de execução (resumo)

1. Subir/conectar PostgreSQL.
2. Subir backend FastAPI.
3. Aplicar seed de dados.
4. Subir frontend Next.js.
5. Acessar UI e validar endpoints.

---

## 6) Passo a passo — execução com Docker

### 6.1 Subir serviços
```bash
docker compose up --build -d
```

### 6.2 Aplicar seed no banco
```bash
docker compose exec backend python scripts_seed.py
```

### 6.3 Verificar saúde da API
```bash
curl http://localhost:8000/health
```

### 6.4 Acessar aplicações
- Frontend: http://localhost:3000
- Swagger (API): http://localhost:8000/docs

### 6.5 Credenciais de demonstração
- Usuário: `admin@portalobra.local`
- Senha: `admin123`

### 6.6 Encerrar ambiente
```bash
docker compose down
```

Se quiser remover também volume do banco:
```bash
docker compose down -v
```

---

## 7) Passo a passo — execução local sem Docker

### 7.1 Banco PostgreSQL
Crie banco e usuário (ajuste conforme sua instalação):

```sql
CREATE DATABASE portal_obra;
CREATE USER portal WITH PASSWORD 'portal';
GRANT ALL PRIVILEGES ON DATABASE portal_obra TO portal;
```

### 7.2 Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure variáveis para sessão atual (exemplo):

```bash
export DATABASE_URL="postgresql+psycopg2://portal:portal@localhost:5432/portal_obra"
export SECRET_KEY="super-secret"
export SCHEDULER_ENABLED="true"
export SCHEDULER_INTERVAL_MINUTES="15"
export SHAREPOINT_MODE="mock"
```

Suba a API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Em outro terminal, aplique seed:

```bash
cd backend
source .venv/bin/activate
python scripts_seed.py
```

### 7.3 Frontend

```bash
cd frontend
npm install
```

Configure variável da API (Linux/macOS):

```bash
export NEXT_PUBLIC_API_URL="http://localhost:8000/api/v1"
npm run dev
```

Acesse: http://localhost:3000

---

## 8) Dependências por camada

### Backend (`backend/requirements.txt`)
- `fastapi`, `uvicorn`
- `sqlalchemy`, `psycopg2-binary`, `alembic`
- `pydantic-settings`
- `pandas`, `openpyxl`
- `apscheduler`
- `python-jose`, `passlib`, `python-multipart`

### Frontend (`frontend/package.json`)
- `next`, `react`, `react-dom`
- `tailwindcss`, `postcss`, `autoprefixer`
- `axios`
- `recharts`
- `@tanstack/react-table`

---

## 9) Rotas principais

### Frontend
- `/login`
- `/dashboard`
- `/planejamento`
- `/engenharia`
- `/orcamento`
- `/medicao`
- `/suprimentos`
- `/campo`
- `/pendencias`
- `/documentos`
- `/busca`
- `/alertas`
- `/admin`

### API (prefixo `/api/v1`)
- `POST /auth/login`
- `GET /dashboard`
- `GET /planejamento`
- `GET /engenharia`
- `GET /orcamento`
- `GET /medicao`
- `GET /suprimentos`
- `GET /campo`
- `GET /pendencias`
- `GET /documentos`
- `GET /busca?q=...`
- `GET /alertas`
- `GET /admin/status`
- `POST /admin/run-ingestion`
- `POST /apontamentos`

---

## 9.1) Modelo de dados analítico (fatos e dimensões)

Foi adicionada uma modelagem dimensional para analytics em `backend/app/models/entities.py` com documentação em `backend/docs/dimensional_model.md` (função de cada tabela e relacionamentos).


## 10) Ingestão SharePoint (somente leitura)

Arquivo de referência: `backend/app/ingestion/sharepoint_adapter.py`.

### Princípios implementados
- Adapter dedicado read-only.
- Sem qualquer escrita na origem.
- Controle incremental por data de modificação + hash/caminho (reprocessa apenas arquivos alterados).
- Registro de rastreabilidade de arquivo origem (`arquivos_origem`).
- Log de execução em `logs_processamento`.
- Atualização automática da base analítica (tabelas fato/dimensão) apenas para os arquivos reprocessados.

### Evolução recomendada
- Substituir mock por Microsoft Graph API.
- Incluir autenticação segura (client credentials).
- Tratar paginação e limites de rate.
- Expandir parser para PDFs/textos futuramente.

---

## 11) Troubleshooting

### `npm install` falha com 403 no ambiente
- Verifique proxy corporativo/Nexus/Artifactory.
- Confirme acesso ao `https://registry.npmjs.org`.
- Se necessário, configure `.npmrc` com registry interno permitido.

### Backend não conecta no banco
- Confirme `DATABASE_URL`.
- Verifique se PostgreSQL está ativo e aceitando conexão na porta 5432.

### Frontend não carrega dados
- Valide `NEXT_PUBLIC_API_URL`.
- Teste `http://localhost:8000/health` e `/docs`.

---

## 12) Scripts úteis

Na raiz do projeto:

```bash
./scripts/bootstrap.sh start
```

Comandos disponíveis:

```bash
./scripts/bootstrap.sh stop
./scripts/bootstrap.sh restart
```

O bootstrap agora:
- sobe o Postgres via Docker Compose;
- cria `backend/.venv`, instala `requirements.txt` e inicia o FastAPI localmente;
- aplica seed local (`backend/scripts_seed.py`);
- instala dependências do frontend e inicia o Next.js localmente;
- grava logs em `.runtime/backend.log` e `.runtime/frontend.log`.

---

## 13) Próximos passos técnicos

1. Completar migrations Alembic para todo schema.
2. Implementar RBAC completo (perfis/permissões por rota).
3. Conectar todas páginas com endpoints reais e filtros globais avançados.
4. Expandir busca global com índice textual e relevância.
5. Adicionar suíte de testes (backend + frontend + e2e).

---

## 14) Licença / uso interno

Projeto base para uso interno e evolução contínua do acompanhamento de obra industrial.

## 15) Gerar pacote ZIP para abrir no VS Code

Para gerar um artefato compactado com tudo necessário para execução local:

```bash
./scripts/create_release_zip.sh
```

O comando cria um arquivo em `dist/` contendo:
- `frontend/`
- `backend/`
- `scripts/`
- `README.md`
- `docker-compose.yml`
- `.env.example`

Abra a pasta extraída no VS Code e siga o passo a passo deste README.

---

