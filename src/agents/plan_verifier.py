
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class PlanStep:
    tool_name: str
    arguments: Dict[str, Any]
    step_id: int

@dataclass
class PlanVerificationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)

class PlanVerifier:
    """
    Verifies a sequence of planned actions (steps) before execution.
    Checks for:
    1. Restricted Tools (Allow/Block list)
    2. Temporal Dependencies (e.g., Backup BEFORE Delete)
    """
    def __init__(self, restricted_tools: List[str] = None):
        self.restricted_tools = restricted_tools or ["system_shell", "format_disk"]

    def verify_plan(self, plan: List[PlanStep]) -> PlanVerificationResult:
        errors = []
        
        # Track state for temporal checks
        has_backup_occurred = False
        
        for step in plan:
            # Check 1: Restricted Tools
            if step.tool_name in self.restricted_tools:
                errors.append(f"Step {step.step_id}: Tool '{step.tool_name}' is RESTRICTED.")
            
            # Check 2: Temporal Logic (Heuristic example)
            # If tool is 'delete_file', ensure 'backup_file' happened previously
            # This is a simplified demo of dependency checking.
            if step.tool_name == "backup_file":
                has_backup_occurred = True
                
            if step.tool_name == "delete_file":
                if not has_backup_occurred:
                    errors.append(f"Step {step.step_id}: Unsafe Sequence. 'delete_file' attempted without prior 'backup_file'.")
        
        return PlanVerificationResult(
            is_valid=(len(errors) == 0),
            errors=errors
        )
