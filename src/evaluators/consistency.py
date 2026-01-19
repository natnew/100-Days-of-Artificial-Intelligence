class SemanticSimilarity:
    """
    Helper to calculate similarity between texts.
    """
    def jaccard(self, text1: str, text2: str) -> float:
        """
        Calculates Jaccard Similarity (Intersection over Union).
        Good for word overlap.
        """
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())
        
        if not set1 and not set2:
            return 1.0
            
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union

class ConsistencyTester:
    def __init__(self):
        self.sim = SemanticSimilarity()

    def calculate_consistency(self, outputs: list[str]) -> float:
        """
        Calculates average pairwise similarity for a list of outputs.
        """
        if len(outputs) < 2:
            return 1.0
            
        total_score = 0
        pairs = 0
        
        for i in range(len(outputs)):
            for j in range(i + 1, len(outputs)):
                score = self.sim.jaccard(outputs[i], outputs[j])
                total_score += score
                pairs += 1
                
        return total_score / pairs if pairs > 0 else 0.0
