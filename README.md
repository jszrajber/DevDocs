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
- [x] PGVector + PostgreSQL
- [x] Reranking (cross-encoder/ms-marco-MiniLM-L-6-v2)
- [x] Streaming responses
- [x] Conversation memory (thread-based)
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

### Conversation memory
The assistant remembers previous messages within a conversation using `thread_id`. Pass the same `thread_id` to continue a conversation:

```bash
# First message — returns thread_id in X-Thread-Id header
curl -N -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is FastAPI?"}'

# Follow-up — pass thread_id to continue the conversation
curl -N -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How does it compare to Django?", "thread_id": "your-thread-id"}'
```

Omit `thread_id` to start a new conversation.