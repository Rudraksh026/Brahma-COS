# BRAHMA COS MVP

Integrated Cognitive Operating System MVP combining Next.js, FastAPI, LangGraph, PostgreSQL/pgvector (or SQLite for local fallback), Ollama/LiteLLM, KOSH knowledge retrieval, memory, governance, execution and audit.

## Stack
- Frontend: Next.js + TypeScript + Tailwind
- Backend: FastAPI + SQLAlchemy
- Agents: LangGraph + LiteLLM + Ollama (`llama3.2:3b`)
- Data: PostgreSQL + pgvector, with SQLite fallback for local development

## Run locally

### Option A: PostgreSQL with Docker (recommended)
1. Start database from the repository root:
```bash
docker compose up -d
```
2. Create `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:12345678@localhost:5433/brahma_cos
LLM_MODEL=ollama/llama3.2:3b
OLLAMA_API_BASE=http://127.0.0.1:11434
```

### Option B: SQLite fallback
Leave `DATABASE_URL` empty in `backend/.env`. The backend automatically uses `backend/brahma_cos.db`.

### Ollama
Install Ollama and run:
```bash
ollama serve
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### Backend
From repository root:
```bash
python -m venv backend/venv
# Windows
backend\venv\Scripts\activate
# macOS/Linux
source backend/venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload --port 8000
```
API docs: http://127.0.0.1:8000/docs

### Frontend
In a second terminal:
```bash
npm install
```
Create `.env.local` if needed:
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```
Then:
```bash
npm run dev
```
Open http://localhost:3000/login

Demo login accepts any valid-looking email and a password of at least 6 characters. It is a frontend demo authentication layer, not production identity management.

## Integrated flow
Founder → Next.js → FastAPI → KOSH/SMRITI → KARMA → PRAGYA → MURPHY → MARYADA → Founder approval when required → RACHIT → NIYANTRA/Audit → Frontend

## Notes
- If Ollama is unavailable, the agent workflow fails closed. Knowledge uploads without embeddings are reported as skipped instead of pretending that semantic retrieval succeeded.
- The MVP keeps RACHIT execution simulated.
- Human approval for blocked tasks is exposed through `/tasks/{id}/approve` and `/tasks/{id}/reject`.
