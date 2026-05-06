from langchain_core.prompts import ChatPromptTemplate
from app.config.llm import llm
from langchain_core.output_parsers import StrOutputParser
from ..state import State
from app.config.logger import logger

"""
Summarization node for more than 10 messages.
It focuses on main aspects of conversation and leaves 2 last messages as chat history.
"""

summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the conversation below in 2-3 sentences. Focus on key topics discussed."),
    ("user", "{chat_history}")
])

summarize_chain = summarize_prompt | llm | StrOutputParser()

async def summarize_node(state: State) -> dict:
    question = state["question"]
    chat_history = state.get("chat_history", [])
    
    if len(chat_history) < 10:
        return {}
    
    logger.info(f"Question: {question} will be summarized")
        
    history_str = "\n".join([
        f"{msg.type}: {msg.content}" for msg in chat_history
    ])
    
    summary = await summarize_chain.ainvoke({"chat_history": history_str})
    
    # Leave last 2 messages and summary
    return {
        "summary": summary,
        "chat_history": chat_history[-2:]
    }
        
        