"""Entry point for Silicon-Agent Plan A cloud swarm."""

import argparse
from dotenv import load_dotenv
from workflows.langgraph_pipeline import build_pipeline
from agents.orchestrator import DesignState

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Silicon-Agent Plan A: Cloud Stack")
    parser.add_argument("--target", required=True, help="Target block name (e.g. ofdm_modulator)")
    parser.add_argument("--spec", required=True, help="3GPP spec reference (e.g. TS 36.211 Section 6.3)")
    parser.add_argument("--max-retries", type=int, default=8, help="Max retry iterations per block")
    args = parser.parse_args()
    
    print(f"Starting Silicon-Agent Plan A for block: {args.target}")
    print(f"Spec reference: {args.spec}")
    
    pipeline = build_pipeline()
    state = DesignState(
        project_phase="spec",
        block_registry={args.target: "PENDING"},
        spec_context=[args.spec]
    )
    
    result = pipeline.invoke(state)
    print("Workflow complete:", result)


if __name__ == "__main__":
    main()
