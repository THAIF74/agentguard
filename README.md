# 🛡️ AgentGuard

Runtime policy enforcement and tamper-proof audit logs for AI agents. Blocks dangerous tool calls before they execute.

## Why?
AI agents are powerful but unpredictable. They can accidentally run m -rf /, leak data, or overspend. Existing tools only *observe* (logging). AgentGuard *enforces* rules at runtime and provides a cryptographic audit trail.

## Features
- **Policy Engine:** Define YAML rules (e.g., block m -rf, limit payments to ).
- **Tamper-Proof Audit Log:** Cryptographically chained logs that detect if anyone tries to alter history.
- **Live Dashboard:** Real-time web UI showing agent actions.
- **Kill Switch:** Instantly freeze a rogue agent with a big red button.

## Quick Start
 `bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the live dashboard
python -m uvicorn agentguard.server:app --reload

# 3. In a second terminal, run the demo agent
python -m examples.demo_agent
 `

## How it works
1. The Guard interceptor wraps your agent's tools.
2. Before any tool runs, it checks policies.yaml.
3. It checks if the system is frozen (.frozen file).
4. Every decision is logged with a SHA-256 hash chain in udit.db.
