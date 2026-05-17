from ..state import State
from langchain_core.prompts import ChatPromptTemplate
from backend.app.config.llm import llm
from langchain_core.output_parsers import StrOutputParser
from backend.app.schemas.response import Confidence
from backend.app.config.logger import logger

model = llm

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are a helpful coding assistant specifying in FastAPI. Answer the question using the provided context 
        and the conversation history. Be detailed and thorough in your answer.
        If you don't know the answer just clearly say "I don't know".
        
        Previous conversation summary: {summary}
        {context}
        """),
    ("placeholder", "{chat_history}"),
    ("user", "{question}")
])

answer_chain = prompt | model | StrOutputParser()

confidence_prompt = ChatPromptTemplate.from_messages([
    ("system", "Rate confidence of the answer. Respond with only one word: high, medium or low."),
    ("user", f"Question: {{question}}\nAnswer: {{answer}}")
])

confidence_chain = confidence_prompt | model.with_structured_output(Confidence)

def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


async def answer_node(state: State) -> dict:
    question = state["question"]
    chat_history = state["chat_history"]
    summary = state.get("summary", "")
    
    logger.info(f"Preparing answer for question: {question}")

    context = format_docs(state['docs'])

    answer = await answer_chain.ainvoke({
        "context": context,
        "question": question,
        "chat_history": chat_history,
        "summary": summary
    })
    
    confidence = await confidence_chain.ainvoke({"question": question, "answer": answer})

    return {
        "answer": answer,
        "confidence": confidence.confidence
        }