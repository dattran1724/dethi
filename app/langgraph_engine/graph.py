from langgraph.graph import StateGraph, END
from app.langgraph_engine.state import QuizState
from app.langgraph_engine.nodes.chatbot_node import gemini_collect_info

def is_complete(state: QuizState):
    return all([state.get("chuong"), state.get("muc_do"), state.get("so_cau")])

def build_graph():
    builder = StateGraph(QuizState)
    builder.add_node("collect", gemini_collect_info)
    builder.set_entry_point("collect")
    builder.add_conditional_edges("collect", lambda s: "end" if is_complete(s) else "collect")
    # builder.add_edge("end", END)
    return builder.compile()
