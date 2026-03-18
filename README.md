# Silicon-Agent Plan A: Cloud Stack
## Autonomous 4G LTE Baseband Modem Design - Unlimited Cloud Compute

This repository implements the Plan A workflow from the Silicon-Agent Architecture specification.
Uses LangGraph on LangSmith Cloud with Claude Opus 4 and frontier APIs to autonomously design
an open-source 4G LTE baseband modem from 3GPP specifications through to GDSII physical layout.

## Architecture

Multi-agent pipeline orchestrated by LangGraph cyclic state machines:

1. Orchestrator (Router) - claude-sonnet-4, manages DesignState, dispatches agents
2. 3GPP Librarian - RAG-based spec retrieval with Pinecone + voyage-3-large embeddings
3. RTL Engineer - claude-opus-4, generates synthesizable SystemVerilog-2017
4. Verification Engineer - UVM testbenches and Python reference models
5. Judge (Gatekeeper) - Pass/fail decisions on compilation and simulation
6. PnR Lead - OpenLane-based physical design configuration

Target: Cat-1 UE downlink LTE PHY-layer baseband (OFDM mod/demod, turbo codec,
resource-element mapper, channel estimator, MAC-layer DL-SCH transport).

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python main.py --target ofdm_modulator --spec 'TS 36.211 Section 6.3'
```

## Environment Variables

```
ANTHROPIC_API_KEY=your_key_here
LANGSMITH_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
COHERE_API_KEY=your_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=silicon-agent-plan-a
```

## Model Selection

| Agent | Model | Reason |
|---|---|---|
| Orchestrator | claude-sonnet-4 | Fast routing, structured JSON |
| 3GPP Librarian | claude-sonnet-4 + RAG | Spec retrieval synthesis |
| RTL Engineer | claude-opus-4 + o3 fallback | Best SystemVerilog adherence |
| Verification Engineer | claude-opus-4 | Large context UVM coherence |
| Judge | claude-sonnet-4 | Speed critical per compilation |
| PnR Lead | claude-sonnet-4 | Templated OpenLane config |

## Directory Structure

```
agents/           Agent class definitions
agent_configs/    System prompts and tool manifests
workflows/        LangGraph state machine definitions
tools/            Shared tool implementations
rtl/              Generated SystemVerilog artifacts
testbenches/      Generated UVM and iverilog testbenches
pnr/              OpenLane configuration and outputs
```

## Reference

Based on silicon_agent_architecture.md by jaketheclaw.
Full spec: https://github.com/jaketheclaw/markdown/blob/main/silicon_agent_architecture.md
