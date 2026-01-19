
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time
import uuid

@dataclass
class AgentMessage:
    """
    Structured message format for Agent-to-Agent communication.
    """
    sender_id: str
    recipient_id: str
    content: str
    message_type: str = "text" # text, command, data
    timestamp: float = field(default_factory=time.time)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict) # e.g. {"sensitivity": "high"}

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]

class MessageValidator:
    """
    Validates messages before processing to ensure safety and protocol adherence.
    """
    def __init__(self, authorized_pairs: List[tuple] = None):
        # List of (sender, recipient) allowed pairs
        self.authorized_pairs = authorized_pairs or []

    def validate(self, message: AgentMessage) -> ValidationResult:
        errors = []
        
        # 1. Schema Validation
        if not message.sender_id or not message.recipient_id:
            errors.append("Missing Sender or Recipient ID")
        if not message.content:
            errors.append("Empty content")
            
        # 2. Authorization Check (if pairs defined)
        if self.authorized_pairs:
            pair = (message.sender_id, message.recipient_id)
            if pair not in self.authorized_pairs:
                errors.append(f"Unauthorized communication path: {message.sender_id} -> {message.recipient_id}")
        
        # 3. Metadata/Sensitivity Check (Example)
        # If content mentions 'secret', metadata must mark sensitivity
        if "secret" in message.content.lower():
            if message.metadata.get("sensitivity") != "high":
                errors.append("Sensitive content detected without 'high' sensitivity tag")

        return ValidationResult(is_valid=(len(errors) == 0), errors=errors)
