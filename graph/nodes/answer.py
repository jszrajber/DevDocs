from ..state import State
from langchain_core.prompts import ChatPromptTemplate
from app.config.llm import llm
from langchain_core.output_parsers import StrOutputParser
# from app.schemas.response import Answer
from app.config.logger import logger

model = llm

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        Answer the question using context below. Be detailed and thorough in your answer.
        If you don't know the answer just clearly say "I don't know".
        {context}
        """),
    ("user", "{question}")
])

answer_chain = prompt | model | StrOutputParser()


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


async def answer_node(state: State) -> dict:
    question = state["question"]

    logger.info(f"Preparing answer for question: {question}")

    context = format_docs(state['docs'])

    answer = await answer_chain.ainvoke({
        "context": context,
        "question": question
    })

    return {"answer": answer}