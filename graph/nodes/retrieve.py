from ..state import State
from langchain_postgres import PGVector
from app.ingestion.process import embeddings
from app.config.settings import settings
from app.config.logger import logger

vectorstore = PGVector(
        embeddings=embeddings,
        collection_name="devdocs",
        connection=settings.VECTOR_URL,
        use_jsonb=True,
        async_mode=True     # Create async engine for conecting to vector db
    )

retriever = vectorstore.as_retriever(search_kwargs={"k": 10})


async def retrieve_node(state: State) -> dict:
    question = state['question']

    logger.info(f"Retrieving documents for question: {question}")

    documents = await retriever.ainvoke(question)

    return {"docs": documents}
