
import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class ReviewRequest:
    id: str
    content: Any
    confidence_score: float
    reason: str
    status: str = "Pending" # Pending, Approved, Rejected, Modified
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    decision_note: str = ""

class HITLManager:
    """
    Manages the workflow for Human-in-the-Loop verification.
    """
    def __init__(self, escalation_threshold: float = 0.8):
        self.escalation_threshold = escalation_threshold
        self.pending_reviews: Dict[str, ReviewRequest] = {}
        self.processed_reviews: Dict[str, ReviewRequest] = {}

    def analyze_and_route(self, content: Any, confidence_score: float) -> Optional[str]:
        """
        Check if content needs review. 
        Returns request_id if review needed, else None (auto-approve).
        """
        if confidence_score < self.escalation_threshold:
            req_id = str(uuid.uuid4())
            request = ReviewRequest(
                id=req_id,
                content=content,
                confidence_score=confidence_score,
                reason=f"Confidence {confidence_score} < Threshold {self.escalation_threshold}"
            )
            self.pending_reviews[req_id] = request
            return req_id
        return None

    def get_pending_requests(self):
        return list(self.pending_reviews.values())

    def submit_feedback(self, request_id: str, action: str, note: str = "") -> bool:
        """
        Process human feedback.
        Action: Approve, Reject, Modify
        """
        if request_id not in self.pending_reviews:
            return False
            
        request = self.pending_reviews.pop(request_id)
        request.status = action
        request.decision_note = note
        self.processed_reviews[request_id] = request
        return True
