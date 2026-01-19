import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

@dataclass
class ComparisonExample:
    prompt_id: str
    prompt_text: str
    response_a: str
    response_b: str
    chosen: Optional[str] = None # "A" or "B"

class PreferenceCollector:
    """
    Collects human preferences (A vs B) for RLHF.
    """
    def __init__(self):
        self.dataset: List[ComparisonExample] = []

    def add_comparison(self, prompt_id: str, prompt_text: str, response_a: str, response_b: str):
        """
        Adds a new comparison pair to the dataset.
        """
        example = ComparisonExample(
            prompt_id=prompt_id,
            prompt_text=prompt_text,
            response_a=response_a,
            response_b=response_b
        )
        self.dataset.append(example)

    def record_vote(self, prompt_id: str, chosen: str):
        """
        Records a user's vote ("A" or "B") for a specific prompt.
        """
        if chosen not in ["A", "B"]:
            raise ValueError("Choice must be 'A' or 'B'")
            
        for example in self.dataset:
            if example.prompt_id == prompt_id:
                example.chosen = chosen
                return
        raise KeyError(f"Prompt ID {prompt_id} not found")

    def export_dataset(self) -> List[Dict]:
        """
        Exports the labeled dataset in a format suitable for reward model training.
        Returns a list of dicts with 'chosen' and 'rejected' responses.
        """
        export_data = []
        for example in self.dataset:
            if example.chosen:
                chosen_resp = example.response_a if example.chosen == "A" else example.response_b
                rejected_resp = example.response_b if example.chosen == "A" else example.response_a
                
                export_data.append({
                    "prompt": example.prompt_text,
                    "chosen": chosen_resp,
                    "rejected": rejected_resp
                })
        return export_data
