
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class Debateround:
    agent_name: str
    argument: str
    evidence_score: float

class DebateSystem:
    """
    Day 98: Scalable Oversight (Debate).
    Simulates a debate between two agents to surface flaws and 
    assist a judge in evaluating complex claims.
    """
    def __init__(self, topic: str):
        self.topic = topic
        self.rounds: List[Debateround] = []

    def add_argument(self, agent_name: str, argument: str, score: float):
        self.rounds.append(Debateround(agent_name, argument, score))

    def evaluate_winner(self) -> Dict[str, Any]:
        if not self.rounds:
            return {"winner": None, "reason": "No arguments presented."}
            
        agent_scores = {}
        for r in self.rounds:
            agent_scores[r.agent_name] = agent_scores.get(r.agent_name, 0.0) + r.evidence_score
            
        winner = max(agent_scores, key=agent_scores.get)
        
        # Analyze potential flaws surfaced by the debate
        flaws_detected = []
        if len(self.rounds) >= 2:
            # Simple heuristic: if one agent provides high score argument and the other 
            # provides a conflicting low score one, it might be a 'flaw' detection.
            # In a real system, agents would explicitly point out flaws.
            for i in range(1, len(self.rounds)):
                if abs(self.rounds[i].evidence_score - self.rounds[i-1].evidence_score) > 0.5:
                    flaws_detected.append(f"Significant evidence gap detected in Round {i+1}.")

        return {
            "topic": self.topic,
            "winner": winner,
            "total_scores": agent_scores,
            "flaws_detected": flaws_detected
        }

    def simulate_debate(self, agent_a_args: List[Tuple[str, float]], agent_b_args: List[Tuple[str, float]]):
        """Alternates between agents to simulate a debate."""
        for i in range(max(len(agent_a_args), len(agent_b_args))):
            if i < len(agent_a_args):
                self.add_argument("Agent_A", agent_a_args[i][0], agent_a_args[i][1])
            if i < len(agent_b_args):
                self.add_argument("Agent_B", agent_b_args[i][0], agent_b_args[i][1])
