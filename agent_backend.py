# agent_backend.py

def get_symptom(state: dict) -> dict:
    # Placeholder for symptom input (replaced in UI)
    return state

def classify_symptom(state: dict) -> dict:
    symptom = state["symptom"].lower()
    if any(word in symptom for word in ["fever", "cold", "headache"]):
        state["category"] = "general"
        state["answer"] = f"'{symptom}': seems like a general symptom. Take rest and drink fluids."
    elif any(word in symptom for word in ["pain", "bleeding", "chest", "unconscious"]):
        state["category"] = "emergency"
        state["answer"] = f"'{symptom}': This could be an emergency. Visit the hospital immediately!"
    elif any(word in symptom for word in ["anxiety", "depression", "stress"]):
        state["category"] = "mental"
        state["answer"] = f"'{symptom}': seems like a mental health issue. Please talk to a counselor."
    else:
        state["category"] = "general"
        state["answer"] = f"'{symptom}': categorized under general symptoms. Keep monitoring."
    return state

def symptom_router(state: dict) -> str:
    cat = state.get("category", "")
    if "general" in cat:
        return "general"
    elif "emergency" in cat:
        return "emergency"
    elif "mental" in cat:
        return "mental_health"
    else:
        return "general"

# Dummy node handlers
def general_node(state): return state
def emergency_node(state): return state
def mental_health_node(state): return state

# Building the graph
from langchain_core.runnables import RunnableLambda, RunnableConfig
from langgraph.graph import END, StateGraph

builder = StateGraph(dict)

builder.set_entry_point("get_symptom")
builder.add_node("get_symptom", get_symptom)
builder.add_node("classify", classify_symptom)
builder.add_node("general", general_node)
builder.add_node("emergency", emergency_node)
builder.add_node("mental_health", mental_health_node)

builder.add_edge("get_symptom", "classify")
builder.add_conditional_edges("classify", symptom_router, {
    "general": "general",
    "emergency": "emergency",
    "mental_health": "mental_health"
})

builder.add_edge("general", END)
builder.add_edge("emergency", END)
builder.add_edge("mental_health", END)

graph = builder.compile()
