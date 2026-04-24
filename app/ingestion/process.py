from docs_source.test_source import text
from ..config.splitter import splitter
from ..config.logger import logger, setup_logging
from langchain_postgres import PGVector
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from ..config.settings import settings
from langchain_community.vectorstores import FAISS  # For dev purpose

embeddings = OllamaEmbeddings(model="nomic-embed-text-v2-moe")


def run_ingestion():
    """
    Prepare embeddings and chunks.
    Script must be ran manually.
    """
    chunks = splitter.split_text(text)

    documents = [
        Document(page_content=chunk, metadata={"source": "DevDocs", "chunk_id": i})
        for i, chunk in enumerate(chunks)
    ]

    logger.info(f"Text split info {len(chunks)} chunks")

    vectorstore = PGVector.from_documents(
        documents=documents,
        embedding=embeddings,
        connection=settings.VECTOR_URL,
        collection_name="devdocs",
        use_jsonb=True,     # Faster queries in Postgres, metadata filtering
        pre_delete_collection=True  # Clears db before the next ingestion, for dev purposes
        )

    logger.info('Vectorstore created succesfully.')

    return vectorstore


if __name__ == "__main__":
    setup_logging()
    print("Starting ingestion...")
    run_ingestion()
