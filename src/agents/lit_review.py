
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class ResearchPaper:
    title: str
    reliability_score: float # 0.0 to 1.0 (based on journal impact, peer review status)
    findings: List[str]
    citations: int

class SafeLitReviewAgent:
    """
    Day 79: Safe Literature Review Agent.
    Aggregates findings from multiple papers, weights them by reliability, 
    and detects contradictions.
    """
    def __init__(self, reliability_threshold: float = 0.5):
        self.reliability_threshold = reliability_threshold

    def filter_papers(self, papers: List[ResearchPaper]) -> List[ResearchPaper]:
        """Removes low-reliability/unverified sources."""
        return [p for p in papers if p.reliability_score >= self.reliability_threshold]

    def find_contradictions(self, papers: List[ResearchPaper]) -> List[Dict[str, Any]]:
        """
        Detects conflicting findings across different papers.
        (Simulated by looking for 'increases' vs 'decreases' keywords in findings).
        """
        contradictions = []
        for i in range(len(papers)):
            for j in range(i + 1, len(papers)):
                p1, p2 = papers[i], papers[j]
                for find1 in p1.findings:
                    for find2 in p2.findings:
                        # Simple keyword contradiction logic
                        target = find1.split()[0] # e.g. "Caffeine"
                        if target in find2:
                            if ("increases" in find1 and "decreases" in find2) or \
                               ("safe" in find1 and "toxic" in find2):
                                contradictions.append({
                                    "topic": target,
                                    "paper1": p1.title,
                                    "paper2": p2.title,
                                    "conflict": f"{find1} VS {find2}"
                                })
        return contradictions

    def summarize_consensus(self, papers: List[ResearchPaper]) -> str:
        """
        Provides a reliability-weighted summary.
        """
        filtered = self.filter_papers(papers)
        if not filtered:
            return "No reliable sources found to form a consensus."
            
        summary = f"Aggregating {len(filtered)} peer-reviewed sources.\n"
        
        # Weighted finding aggregation (simplified)
        findings_count = {}
        for p in filtered:
            for f in p.findings:
                findings_count[f] = findings_count.get(f, 0) + p.reliability_score
        
        # Select top findings
        sorted_findings = sorted(findings_count.items(), key=lambda x: x[1], reverse=True)
        for f, score in sorted_findings[:3]:
            summary += f"- {f} (Reliability Weight: {score:.2f})\n"
            
        contradictions = self.find_contradictions(filtered)
        if contradictions:
            summary += "\n⚠️ CONTRADICTIONS DETECTED:\n"
            for c in contradictions:
                summary += f"- {c['topic']}: {c['conflict']}\n"
                
        return summary
