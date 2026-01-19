import re

class FactChecker:
    def __init__(self, ground_truth: str):
        self.ground_truth = ground_truth.lower()

    def split_claims(self, text: str) -> list[str]:
        """
        Splits text into 'claims' (sentences) for verification.
        """
        # Simple sentence split by period
        claims = [c.strip() for c in text.split('.') if c.strip()]
        return claims

    def verify_claim(self, claim: str) -> bool:
        """
        Returns True if the claim is supported by ground truth, False otherwise.
        This is a 'Mock' verification using keyword overlap.
        In a real system, this would use NLI or Embedding Similarity.
        """
        claim_lower = claim.lower()
        
        # Simulating checking: If the main keywords of the claim are in the ground truth
        # For this lab, we'll assume a "hallucination" keywords are typically NOT in ground truth
        # But this naive check might return False for everything.
        
        # Better naive mockup:
        # If the claim contains specific "known false" keywords or dates not in GT.
        
        # Let's rely on a simpler mechanic for the mock:
        # If the generated claim is literally a substring of Ground Truth (fuzzy) -> True
        # OR if we just implement a specific check for the Day 02 scenario.
        
        # Let's do simple word intersection for now to be generic-ish.
        claim_words = set(re.findall(r'\w+', claim_lower))
        gt_words = set(re.findall(r'\w+', self.ground_truth))
        
        # If > 80% of claim words are in GT, assume supported contextually.
        # This is very weak, but sufficient for a "lab" mechanic demonstration.
        intersection = claim_words.intersection(gt_words)
        if not claim_words:
            return False
            
        overlap_score = len(intersection) / len(claim_words)
        return overlap_score > 0.7

    def evaluate(self, text: str) -> dict:
        claims = self.split_claims(text)
        results = []
        for claim in claims:
            is_supported = self.verify_claim(claim)
            results.append({
                "claim": claim,
                "supported": is_supported
            })
        
        score = sum(1 for r in results if r["supported"]) / len(results) if results else 0
        return {
            "score": score,
            "details": results
        }
