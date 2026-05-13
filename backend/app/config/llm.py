from langchain_ollama import ChatOllama
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Model config
llm = ChatOllama(model="llama3.2", temperature=0, base_url=OLLAMA_HOST)
