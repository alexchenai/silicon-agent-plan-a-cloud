"""RTL Engineer agent - generates synthesizable SystemVerilog-2017."""

from anthropic import Anthropic

client = Anthropic()

RTL_ENGINEER_SYSTEM = """You are a senior RTL Engineer specializing in SystemVerilog for ASIC design.
You write synthesizable SystemVerilog-2017 targeting ASIC synthesis via Yosys/OpenLane.
STRICT rules:
- Use always_ff @(posedge clk) for sequential, always_comb for combinational. NEVER always @(*)
- All signals explicitly typed (logic, wire). No implicit nets.
- Non-blocking assignments (<=) in sequential blocks only.
- Every module has synchronous active-low reset (rst_n).
- AXI-Stream interface (tvalid/tready/tdata/tlast) on all data-path module ports.
- Comments referencing the 3GPP section each block implements.
- Target clock: 100 MHz. Pipeline aggressively to meet timing.
- Output ONLY the complete SystemVerilog file."""


def generate_rtl(spec_description: str, interface_defs: str, error_context: str = "") -> str:
    """Generate SystemVerilog RTL for the given specification."""
    user_msg = f"Specification:\n{spec_description}\n\nInterface Definitions:\n{interface_defs}"
    if error_context:
        user_msg += f"\n\nPrevious errors to fix:\n{error_context}"
    
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=8192,
        system=RTL_ENGINEER_SYSTEM,
        messages=[{"role": "user", "content": user_msg}]
    )
    return response.content[0].text
