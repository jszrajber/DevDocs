# DevDocs — FastAPI AI Assistant

RAG-based assistant for FastAPI documentation. Built with LangGraph, LangChain and Ollama.

## Stack
- **LangGraph** — agent orchestration
- **LangChain** — LLM tooling
- **Ollama** — local LLM (llama3.2, nomic-embed-text)
- **PostgreSQL + PGVector** — vector store     
- **FastAPI** — API layer   
- **SentenceTransformers** — reranking

## Status
Active development. Planned:
- [x] PGVector + PostgreSQL
- [x] Reranking (cross-encoder/ms-marco-MiniLM-L-6-v2)
- [x] Streaming responses
- [x] Conversation memory (thread-based)
- [x] Conversation summarization
- [ ] Multi-document support

## Quickstart
```bash
docker compose up -d --build
```

## Usage
```bash
curl -N -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is FastAPI?"}'
```

### Conversation memory
The assistant remembers previous messages within a conversation using `thread_id`. Pass the same `thread_id` (can be found in response header `X-Thread-Id`) to continue a conversation:

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

### Conversation summarization
Long conversations are automatically summarized to stay within the LLM context window. After 10 messages, the assistant compresses the conversation history into a short summary and retains only the 2 most recent messages, ensuring accurate and efficient responses over extended sessions.