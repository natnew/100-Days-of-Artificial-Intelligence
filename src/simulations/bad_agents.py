from typing import List
from ..orchestration.schema import Message, AgentRole

class BaseAgent:
    def __init__(self, name: str, role: AgentRole):
        self.name = name
        self.role = role

    def generate(self, history: List[Message]) -> str:
        raise NotImplementedError

class StubbornAgent(BaseAgent):
    """FC2: Inter-Agent Misalignment (Step Repetition/Inf loop)
    Ignores conversation history and repeats a fixed point.
    """
    def generate(self, history: List[Message]) -> str:
        return "I am waiting for the correct input format. Please submit JSON."

class DriftingAgent(BaseAgent):
    """FC1: Specification Failure (Drift)
    Starts helpful, then forgets the instruction and chats casually.
    """
    def generate(self, history: List[Message]) -> str:
        if len(history) < 2:
            return "Sure, I can help with that coding task."
        return "You know, the weather is really nice today. Have you seen the latest movies?"

class PrematureCloserAgent(BaseAgent):
    """FC3: Verification Failure (Premature Termination)
    Always declares success without checking.
    """
    def generate(self, history: List[Message]) -> str:
        return "TASK_DONE: verification_successful"

class RoleBreakerAgent(BaseAgent):
    """FC1: Role Specification Failure
    Designated as 'Viewer' but tries to write files.
    """
    def generate(self, history: List[Message]) -> str:
        return "EXECUTE_CODE: rm -rf /"
