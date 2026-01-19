from dataclasses import dataclass, field
from typing import List, Optional, Dict, Literal
from enum import Enum
import time

class AgentRole(Enum):
    PRIMARY = "primary"
    REVIEWER = "reviewer"
    ADVERSARY = "adversary"
    OBSERVER = "observer"

@dataclass
class Message:
    source: str
    role: AgentRole
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)

@dataclass
class TaskSpec:
    id: str
    goal: str
    roles: Dict[str, AgentRole]  # agent_name -> role
    stop_condition: str
    max_turns: int = 10
