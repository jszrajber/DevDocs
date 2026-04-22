from langgraph.graph import StateGraph, END
from .nodes.retrieve import retrieve_node
from .nodes.is_safe import is_safe_node
from .nodes.reranker import reranker_node
from .nodes.answer import answer_node
from .state import State

graph = StateGraph(State)


def route_safety(state: State) -> str:
    if state["is_safe"] == "true":
        return "continue"
    return "stop"


# Adding nodes
graph.add_node("retrieve", retrieve_node)
graph.add_node("is_safe", is_safe_node)
graph.add_node("reranker", reranker_node)
graph.add_node("answer", answer_node)


graph.set_entry_point("is_safe")
graph.add_conditional_edges(
    "is_safe",
    route_safety,
    {
        "continue": "retrieve",
        "stop": END
    }
)

graph.add_edge("retrieve", "reranker")
graph.add_edge("reranker", "answer")
graph.set_finish_point("answer")

# Compile graph
graph_app = graph.compile()
