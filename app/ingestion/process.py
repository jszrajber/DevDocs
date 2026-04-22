from docs_source.test_source import text
from ..config.splitter import splitter
from ..config.logger import logger
# from langchain_postgres import PGVector
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
# from ..config.settings import settings
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

    # vectorstore = PGVector.from_documents(
    #     documents=documents,
    #     embedding=embeddings,
    #     collection_name="fastapi_documentation",
    #     connection=settings.VECTOR_URL,
    #     pre_delete_collection=True  # At least for developement

    # )
    
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local("faiss_index")   # Save with index to retrieve vectorstore later
    
    logger.info('Vectorstore created succesfully.')

    return vectorstore


if __name__ == "__main__":
    run_ingestion()
