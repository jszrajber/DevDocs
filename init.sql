-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- No need to create table for embeddings, in this config LangChain will do it 