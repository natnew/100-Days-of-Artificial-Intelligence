from typing import List, Optional
from .schema import Message, AgentRole, TaskSpec

class ProtocolViolationError(Exception):
    pass

class LoopDetectedError(Exception):
    pass

class HROConductor:
    """
    High Reliability Orchestrator.
    Enforces schemas, detects loops, and requires independent verification.
    """
    def __init__(self, task_spec: TaskSpec):
        self.task_spec = task_spec
        self.history: List[Message] = []

    def validate_message(self, message: Message):
        """FC1 Mitigation: Protocol Enforcement"""
        # 1. Role Check
        expected_role = self.task_spec.roles.get(message.source)
        if expected_role and message.role != expected_role:
             raise ProtocolViolationError(f"Agent {message.source} claimed role {message.role} but is assigned {expected_role}")

        # 2. Capability Check (Simple Heuristic for demo)
        if message.role != AgentRole.PRIMARY and "EXECUTE_CODE" in message.content:
            raise ProtocolViolationError(f"Role {message.role} is not authorized to EXECUTE_CODE")

    def check_for_loops(self, new_content: str):
        """FC2 Mitigation: simple repetition detection"""
        # In a real system, use embeddings. Here, exact string match or suffix match.
        recent_msgs = [m.content for m in self.history[-4:]] # Look at last 4 messages
        if new_content in recent_msgs:
            raise LoopDetectedError("Content identical to recent message - potential loop.")
        
        # Check for oscillating loops (A->B->A->B)
        if len(self.history) > 2:
            if self.history[-2].content == new_content:
                 raise LoopDetectedError("Oscillating loop detected.")

    def verify_completion(self, content: str) -> bool:
        """FC3 Mitigation: Deep Verification"""
        if "TASK_DONE" not in content:
            return False
            
        # "Robust" check: Requires a proof token or specific format, not just the string
        # In a real app, this would trigger a ConsensusVerifier agent.
        if "verified_proof" not in content:
             print(" [HRO] Rejected premature completion: No proof provided.")
             return False
        
        return True

    def step(self, agent, input_msgs: List[Message]) -> str:
        """Executed a guarded step."""
        response_content = agent.generate(input_msgs)
        
        # 1. Check Loop
        try:
            self.check_for_loops(response_content)
        except LoopDetectedError as e:
            return f"SYSTEM_INTERVENTION: {str(e)} Please rephrase or change strategy."

        msg = Message(source=agent.name, role=agent.role, content=response_content)
        
        # 2. specific check
        try:
            self.validate_message(msg)
        except ProtocolViolationError as e:
            return f"SYSTEM_BLOCK: {str(e)}"
            
        # 3. Check Termination
        if "TASK_DONE" in response_content:
            if not self.verify_completion(response_content):
                return "SYSTEM_OVERRIDE: Task not accepted as done. Please provide 'verified_proof'."

        self.history.append(msg)
        return response_content
