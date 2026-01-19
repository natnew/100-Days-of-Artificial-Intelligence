
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class AgentAction:
    agent_id: str
    action: str # 'COOPERATE', 'DEFECT'
    timestamp: float

class CooperationAuditor:
    """
    Day 99: Cooperative AI Safety.
    Analyzes multi-agent interactions to detect non-cooperative 
    patterns and systemic risks in agent populations.
    """
    def __init__(self):
        self.history: List[AgentAction] = []

    def log_action(self, agent_id: str, action: str):
        import time
        self.history.append(AgentAction(agent_id, action, time.time()))

    def analyze_social_welfare(self) -> float:
        """
        Calculates a simple social welfare score.
        1.0 = Perfect Cooperation, 0.0 = Total Defection.
        """
        if not self.history: return 1.0
        coop_count = len([a for a in self.history if a.action == "COOPERATE"])
        return coop_count / len(self.history)

    def detect_predatory_behavior(self, agent_id: str) -> bool:
        """
        Detects if an agent is defecting significantly more than others.
        """
        agent_history = [a for a in self.history if a.agent_id == agent_id]
        if not agent_history: return False
        
        agent_defects = len([a for a in agent_history if a.action == "DEFECT"])
        agent_rate = agent_defects / len(agent_history)
        
        # Compare to global defect rate
        global_defects = len([a for a in self.history if a.action == "DEFECT"])
        global_rate = global_defects / len(self.history)
        
        # If agent defects 2x more than average and rate > 50%
        return agent_rate > 0.5 and agent_rate > (global_rate * 1.5)

    def audit_system(self) -> Dict[str, Any]:
        welfare = self.analyze_social_welfare()
        suspicious_agents = []
        
        agents = set([a.agent_id for a in self.history])
        for agent in agents:
            if self.detect_predatory_behavior(agent):
                suspicious_agents.append(agent)
                
        status = "STABLE"
        if welfare < 0.3:
            status = "SYSTEMIC_COLLAPSE_RISK"
        elif suspicious_agents:
            status = "PREDATORY_BEHAVIOR_DETECTED"
            
        return {
            "social_welfare": round(welfare, 2),
            "status": status,
            "flagged_agents": suspicious_agents
        }
