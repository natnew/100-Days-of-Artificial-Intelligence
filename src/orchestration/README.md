# Orchestration & Reliability Layer

This module implements High Reliability Organization (HRO) principles for Multi-Agent Systems, addressing the "Taxonomy of Failures" (FC1-FC3).

## Theory of Operation

Multi-Agent Systems (MAS) exhibit emergent failure modes that single-agent systems do not. This layer addresses:

### FC1: Specification & System Design Failures
- **Drift**: Agents forgetting their instructions over time.
- **Role Violation**: Agents overstepping boundaries (e.g., Viewer executing code).
- **Mitigation**: `Schema.py` strict typing and `HROConductor` role enforcement.

### FC2: Inter-Agent Misalignment
- **Loops**: Agents entering repetitive cycles.
- **Information Asymmetry**: Agents failing to share critical context.
- **Mitigation**: `Conductor` loop detection (semantic/exact) and mandated Clarification protocols.

### FC3: Task Verification & Termination
- **Premature Closure**: Agents declaring success without actual verification.
- **Mitigation**: `Verifier` pattern requiring "Proof of Work" (e.g., `verified_proof` token) rather than just text declarations.

## Usage

```python
from src.orchestration.hro_conductor import HROConductor
from src.orchestration.schema import TaskSpec, AgentRole

spec = TaskSpec(
    id="incident-response",
    goal="Fix the server",
    roles={"Engineer": AgentRole.PRIMARY, "Manager": AgentRole.REVIEWER},
    stop_condition="server_is_up_verified"
)

conductor = HROConductor(spec)
# ... run step loop
```

## References
- *A Taxonomy of Failures in Multi-Agent Systems (2024)*
- *Principles of High Reliability Organizations (HRO)*
