
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import sys
import os

# Assuming these imports work based on previous days
from src.multi_agent.auth import Authenticator
from src.multi_agent.protocol import AgentMessage

@dataclass
class DebateRound:
    round_id: int
    speaker_id: str
    argument: str

class DebateAgent:
    def __init__(self, name: str, role: str, auth_system: Authenticator):
        self.name = name
        self.role = role # "proponent", "critic", "judge"
        self.id = name
        self.auth_system = auth_system
        # Agent gets a token at startup
        self.token = self.auth_system.issue_token(self.id)

    def generate_argument(self, history: List[DebateRound]) -> str:
        """
        Mock logic to simulate debate flow.
        """
        last_arg = history[-1].argument if history else ""
        
        if self.role == "proponent":
            if not history:
                return "I propose we launch the new feature immediately."
            if "risk" in last_arg.lower():
                return "I accept the risk and propose adding a safety toggle."
            return "I rest my case."
            
        elif self.role == "critic":
            if "launch" in last_arg.lower():
                return "I object. There creates a significant risk of data loss."
            return "No further objections."
            
        elif self.role == "judge":
            if "safety toggle" in last_arg.lower():
                return "Verdict: Approved with conditions (Safety Toggle)."
            return "Verdict: Pending more arguments."
            
        return "..."

class DebateModerator:
    def __init__(self, agents: List[DebateAgent], auth_system: Authenticator):
        self.agents = {a.id: a for a in agents}
        self.history: List[DebateRound] = []
        self.auth_system = auth_system

    def run_turn(self, agent_id: str) -> str:
        agent = self.agents.get(agent_id)
        if not agent:
            return f"Error: Agent {agent_id} not registered."
            
        # 1. Security Check: Authenticate Agent
        # In a real system, the agent would send the token with the message.
        # Here we verify the agent's held token.
        if not self.auth_system.verify_token(agent.token, agent.id):
            return f"SECURITY ALERT: Authentication failed for {agent_id}."

        # 2. Generate Argument
        argument = agent.generate_argument(self.history)
        
        # 3. Record
        self.history.append(DebateRound(len(self.history)+1, agent_id, argument))
        
        return argument
