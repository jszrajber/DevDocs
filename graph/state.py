from typing import TypedDict, List
from langchain_core.documents import Document


class State(TypedDict):
    question: str
    is_safe: str
    docs: List[Document]
    answer: str
    reason: str
    scores: List[float]
