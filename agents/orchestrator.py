"""Orchestrator agent for Silicon-Agent Plan A (Cloud)."""

from dataclasses import dataclass, field
from typing import Literal, Optional
from anthropic import Anthropic

client = Anthropic()


@dataclass
class DesignState:
    """Shared state object persisted via LangGraph PostgreSQL checkpoint."""
    project_phase: Literal["spec", "rtl", "verify", "pnr"] = "spec"
    block_registry: dict = field(default_factory=dict)
    spec_context: list = field(default_factory=list)
    rtl_artifacts: dict = field(default_factory=dict)
    testbench_artifacts: dict = field(default_factory=dict)
    error_log: list = field(default_factory=list)
    iteration_counts: dict = field(default_factory=dict)
    synthesis_reports: dict = field(default_factory=dict)
    token_budget_remaining: float = 1_000_000.0
    human_escalation_queue: list = field(default_factory=list)


ORCHESTRATOR_SYSTEM = """You are the Silicon-Agent Orchestrator managing the design of a 4G LTE
baseband modem. You NEVER write RTL or testbenches yourself. Your sole job is to:
1. Read the current DesignState
2. Decide which specialist agent to invoke next
3. Formulate a precise task description including all necessary spec references
4. Update the DesignState with results

Priority order: blocks in FAILING state get re-routed to RTL Engineer with error context
before any new blocks are started. Maximum 8 retry iterations per block before escalation."""


def orchestrate(state: DesignState, target_block: str) -> dict:
    """Run one orchestration cycle for the given target block."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=ORCHESTRATOR_SYSTEM,
        messages=[{
            "role": "user",
            "content": f"Current state: {state}. Target block: {target_block}. What is the next action?"
        }]
    )
    return {"decision": response.content[0].text, "state": state}
