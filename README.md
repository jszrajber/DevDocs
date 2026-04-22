# DevDocs — FastAPI AI Assistant

RAG-based assistant for FastAPI documentation. Built with LangGraph, LangChain and Ollama.

## Stack
- **LangGraph** — agent orchestration
- **LangChain** — LLM tooling
- **Ollama** — local LLM (llama3.2, nomic-embed-text)
- **FAISS** — vector store (dev), PostgreSQL + PGVector (planned)
- **FastAPI** — API layer

## Status
Active development. Planned:
- [ ] PGVector + PostgreSQL
- [ ] Reranking
- [ ] Streaming responses
- [ ] Multi-document support

## Quickstart
```bash
pip install -r requirements.txt
python -m app.ingestion.process  # build vector index
uvicorn app.main:app --reload
```

## Usage
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I add middleware in FastAPI?"}'
```