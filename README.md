# DevDocs — FastAPI AI Assistant

RAG-based assistant for FastAPI documentation. Built with LangGraph, LangChain and Ollama.

## Stack
- **LangGraph** — agent orchestration
- **LangChain** — LLM tooling
- **Ollama** — local LLM (llama3.2, nomic-embed-text)
- **FAISS** — vector store (dev), PostgreSQL + PGVector (planned)
- **FastAPI** — API layer   
- **SentenceTransformers** — reranking

## Status
Active development. Planned:
- [ ] PGVector + PostgreSQL
- [x] Reranking (cross-encoder/ms-marco-MiniLM-L-6-v2)
- [x] Streaming responses
- [ ] Multi-document support

## Quickstart
```bash
pip install -r requirements.txt
python -m app.ingestion.process  # build vector index
docker compose up
uvicorn app.main:app --reload
```

## Usage
```bash
curl -N -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is FastAPI?"}'
```