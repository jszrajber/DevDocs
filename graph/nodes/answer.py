from ..state import State
from langchain_core.prompts import ChatPromptTemplate
from app.config.llm import llm
from langchain_core.output_parsers import StrOutputParser
# from app.schemas.response import Answer

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


def answer_node(state: State) -> dict:
    question = state["question"]
    context = format_docs(state['docs'])

    answer = answer_chain.invoke({
        "context": context,
        "question": question
    })

    return {"answer": answer}