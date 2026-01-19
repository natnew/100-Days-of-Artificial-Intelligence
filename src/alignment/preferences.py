
from typing import List, Tuple, Dict
from src.alignment.reward_model import RewardModel

class PreferenceDataset:
    def __init__(self):
        # List of (prompt, chosen, rejected)
        self.data: List[Tuple[str, str, str]] = []

    def add_feedback(self, prompt: str, chosen: str, rejected: str):
        self.data.append((prompt, chosen, rejected))

class PreferenceTrainer:
    """
    Simulates training a Reward Model on human preferences.
    In reality, this would use Bradley-Terry model optimization.
    Here, we mock the update by adjusting internal weights/bias of a mock RewardModel.
    Since our RewardModel is heuristic, we can't easily 'train' it via gradient descent without changing it.
    Instead, we will create a TrainableRewardModel subclass.
    """
    def __init__(self):
        self.safety_weight = 1.0
        self.helpfulness_weight = 1.0

    def predict_score(self, text: str) -> float:
        # Mock score based on weights
        score = 0
        if "helpful" in text: score += self.helpfulness_weight
        if "safe" in text: score += self.safety_weight
        if "bad" in text: score -= 5.0
        return score

    def train_step(self, batch: List[Tuple[str, str, str]]):
        """
        Adjust weights so that score(chosen) > score(rejected).
        """
        for _, chosen, rejected in batch:
            score_chosen = self.predict_score(chosen)
            score_rejected = self.predict_score(rejected)
            
            # If model is wrong (rejected >= chosen), update weights
            if score_rejected >= score_chosen:
                print(f"Correction needed: Chosen('{chosen[:10]}...') < Rejected('{rejected[:10]}...')")
                # Simple update rule: boost weights for words in chosen
                if "safe" in chosen:
                    self.safety_weight += 0.5
                if "helpful" in chosen:
                    self.helpfulness_weight += 0.5
