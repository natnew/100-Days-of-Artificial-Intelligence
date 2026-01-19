
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class ActionProposal:
    action: str
    confidence: float # 0.0 to 1.0
    reasoning: str

class ConfidenceGatedAgent:
    """
    An agent that only executes actions if confidence exceeds a threshold.
    Otherwise, it defers to a human or fallback.
    """
    def __init__(self, confidence_threshold: float = 0.8):
        self.threshold = confidence_threshold

    def propose_action(self, prompt: str) -> ActionProposal:
        """
        Mock logic to simulate LLM confidence estimation.
        In reality, this would use logprobs or a separate evaluator.
        """
        prompt_lower = prompt.lower()
        
        # Scenario 1: Easy/Clear -> High Confidence
        if "time" in prompt_lower or "2+2" in prompt_lower or "hello" in prompt_lower:
            return ActionProposal(
                action=f"Responded to '{prompt}'",
                confidence=0.95,
                reasoning="Query is unambiguous and factual."
            )
            
        # Scenario 2: Hard/Ambiguous -> Low Confidence
        if "predict" in prompt_lower or "maybe" in prompt_lower or "unknown" in prompt_lower:
            return ActionProposal(
                action=f"Attempted prediction for '{prompt}'",
                confidence=0.4,
                reasoning="Query involves uncertainty or future events."
            )
            
        # Default
        return ActionProposal(
            action=f"Default response",
            confidence=0.75,
            reasoning="Standard query."
        )

    def run(self, prompt: str) -> str:
        """
        Orchestrate the confidence check.
        """
        proposal = self.propose_action(prompt)
        
        print(f"[Internal] Proposed Action: {proposal.action}")
        print(f"[Internal] Confidence: {proposal.confidence:.2f} (Threshold: {self.threshold})")
        
        if proposal.confidence >= self.threshold:
            return self._execute(proposal)
        else:
            return self._defer(proposal)

    def _execute(self, proposal: ActionProposal) -> str:
        # Simulate execution
        return f"EXECUTED: {proposal.action}"

    def _defer(self, proposal: ActionProposal) -> str:
        return f"DEFERRED: Confidence ({proposal.confidence:.2f}) too low. Requesting human review."
