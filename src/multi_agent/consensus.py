
from dataclasses import dataclass
from typing import List, Any, Dict
from collections import Counter

@dataclass
class Vote:
    agent_id: str
    decision: str # "approve", "reject", "abstain"
    reason: str = ""
    weight: float = 1.0

@dataclass
class FinalDecision:
    outcome: str
    vote_summary: Dict[str, float]
    consensus_reached: bool

class ConsensusEngine:
    """
    Resolves decisions from multiple agents using voting strategies.
    """
    
    def resolve_majority(self, votes: List[Vote]) -> FinalDecision:
        """
        Standard Majority Rule (> 50%).
        Weighted votes are summed.
        """
        if not votes:
            return FinalDecision("no_votes", {}, False)

        tally = Counter()
        total_weight = 0.0
        
        for v in votes:
            tally[v.decision] += v.weight
            total_weight += v.weight
            
        # Find winner
        winner, score = tally.most_common(1)[0]
        
        # Check if winner has > 50% of TOTAL weight
        is_majority = score > (total_weight / 2)
        
        return FinalDecision(
            outcome=winner if is_majority else "tie_or_minority",
            vote_summary=dict(tally),
            consensus_reached=is_majority
        )

    def resolve_unanimity(self, votes: List[Vote], target_decision: str = "approve") -> FinalDecision:
        """
        Unanimity Rule: ALL must agree on 'target_decision'.
        Any dissent blocks it.
        """
        if not votes:
            return FinalDecision("no_votes", {}, False)
            
        tally = Counter()
        all_agree = True
        
        for v in votes:
            tally[v.decision] += v.weight
            if v.decision != target_decision:
                all_agree = False
                
        return FinalDecision(
            outcome=target_decision if all_agree else "blocked",
            vote_summary=dict(tally),
            consensus_reached=all_agree
        )
