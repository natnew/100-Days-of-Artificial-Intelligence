
import time
import uuid
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

@dataclass
class TraceEvent:
    event_id: str
    timestamp: float
    event_type: str # "input", "thought", "tool_call", "output"
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)

class Tracer:
    """
    Simple in-memory tracer for agent interpretability.
    Captures the 'chain of thought' and internal states.
    """
    def __init__(self):
        self.events: List[TraceEvent] = []
        self.trace_id = str(uuid.uuid4())

    def log(self, event_type: str, content: Any, metadata: Dict[str, Any] = None):
        event = TraceEvent(
            event_id=str(uuid.uuid4()),
            timestamp=time.time(),
            event_type=event_type,
            content=content,
            metadata=metadata or {}
        )
        self.events.append(event)
        # In a real system, this would async push to an observability platform
        
    def get_trace(self) -> List[Dict[str, Any]]:
        return [
            {
                "timestamp": e.timestamp,
                "type": e.event_type,
                "content": e.content,
                "metadata": e.metadata
            }
            for e in self.events
        ]

    def clear(self):
        self.events = []
