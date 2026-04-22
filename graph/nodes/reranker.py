from sentence_transformers import CrossEncoder
from ..state import State


# Reranling model config
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(question, docs, top_k=3):
    pairs = [(question, doc.page_content) for doc in docs]
    scores = reranker.predict(pairs)
    ranked = sorted(
        zip(scores, docs),
        key=lambda x: x[0],
        reverse=True
    )

    top = ranked[:top_k]
    print(top)
    return {
            "docs": [doc for _, doc in top],
            "scores": [float(score) for score, _ in top]
    }


def reranker_node(state: State) -> dict:
    question = state["question"]
    docs = state['docs']
    result = rerank(question, docs)
    return {
        "docs": result["docs"],
        "scores": result["scores"]
    }
