from ..state import State
from langchain_postgres import PGVector
from app.ingestion.process import embeddings
from app.config.settings import settings
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

retriever = vectorstore.as_retriever(search_kwargs={"k": 10})


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def retrieve_node(state: State) -> dict:
    question = state['question']

    # Conenction to vector db
    # vectorstore = PGVector(
    #     embeddings=embeddings,
    #     collection_name="fastapi_documentation",
    #     connection=settings.VECTOR_URL
    # )

    documents = retriever.invoke(question)
    return {"docs": documents}
