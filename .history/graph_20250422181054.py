from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_core.runnables import RunnableLambda
from chains.stage_router_chain import get_stage
from chains.response_chain import generate_response
from chains.rag_interface import retrieve_knowledge

# 🔧 状態の定義
class GraphState(TypedDict):
    user_input: str
    stage: str
    knowledge_summary: str
    response: str
    emotional_intensity: int
    conversation_history: List[str]  # 会話履歴を追加

# 🧠 各ノードの処理
def diagnose_stage(state: GraphState) -> dict:
    return {"stage": get_stage(state["user_input"], state["conversation_history"])}

def estimate_emotional_intensity(state: GraphState) -> dict:
    return {"emotional_intensity": 60}

def retrieve_and_summarize(state: GraphState) -> dict:
    return {"knowledge_summary": retrieve_knowledge(state["stage"], state["user_input"])}

def generate_bot_response(state: GraphState) -> dict:
    return {
        "response": generate_response(
            state["stage"],
            state["user_input"],
            state["knowledge_summary"]
        )
    }

# 🔗 グラフ定義
workflow = StateGraph(GraphState)
workflow.add_node("diagnose_stage", RunnableLambda(diagnose_stage))
workflow.add_node("estimate_emotion", RunnableLambda(estimate_emotional_intensity))
workflow.add_node("retrieve_knowledge", RunnableLambda(retrieve_and_summarize))
workflow.add_node("generate_response", RunnableLambda(generate_bot_response))

workflow.set_entry_point("diagnose_stage")
workflow.add_edge("diagnose_stage", "estimate_emotion")
workflow.add_edge("estimate_emotion", "retrieve_knowledge")
workflow.add_edge("retrieve_knowledge", "generate_response")
workflow.add_edge("generate_response", END)

# 🧠 実行本体
app = workflow.compile()
