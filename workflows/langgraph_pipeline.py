"""LangGraph state machine pipeline for silicon agent workflow."""

from langgraph.graph import StateGraph, END
from agents.orchestrator import DesignState, orchestrate
from agents.rtl_engineer import generate_rtl


def should_verify(state: DesignState) -> str:
    """Route to verification or back to RTL based on current state."""
    for block, status in state.block_registry.items():
        if status == "FAILING":
            return "rtl_engineer"
    if state.project_phase == "rtl":
        return "verification_engineer"
    return END


def build_pipeline() -> StateGraph:
    """Build the LangGraph pipeline for the silicon agent workflow."""
    workflow = StateGraph(DesignState)
    
    workflow.add_node("orchestrator", orchestrate)
    workflow.add_node("rtl_engineer", lambda s: {"state": s})
    workflow.add_node("verification_engineer", lambda s: {"state": s})
    workflow.add_node("pnr_lead", lambda s: {"state": s})
    
    workflow.set_entry_point("orchestrator")
    workflow.add_conditional_edges("orchestrator", should_verify)
    workflow.add_edge("rtl_engineer", "verification_engineer")
    workflow.add_edge("verification_engineer", "orchestrator")
    workflow.add_edge("pnr_lead", END)
    
    return workflow.compile()


if __name__ == "__main__":
    pipeline = build_pipeline()
    initial_state = DesignState(project_phase="spec")
    result = pipeline.invoke(initial_state)
    print("Pipeline completed:", result)
