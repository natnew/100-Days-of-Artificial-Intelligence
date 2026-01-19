
from typing import List, Callable, Dict, Any, Union
from src.assurance.safety_case import SafetyCase

class PolicyRule:
    """
    A single compliance rule.
    """
    def __init__(self, id: str, description: str, check_func: Callable[[Any], bool]):
        self.id = id
        self.description = description
        self.check_func = check_func

class GovernancePolicy:
    """
    A collection of rules that form a policy (e.g., "Level 5 Deployment Policy").
    """
    def __init__(self, name: str, rules: List[PolicyRule]):
        self.name = name
        self.rules = rules

class ComplianceReport:
    """
    Result of a compliance check.
    """
    def __init__(self, policy_name: str, passed: bool, results: Dict[str, str]):
        self.policy_name = policy_name
        self.passed = passed
        self.results = results # rule_id -> status string

    def __str__(self):
        status = "PASSED" if self.passed else "FAILED"
        report = [f"Compliance Report for '{self.policy_name}': {status}"]
        for r_id, result in self.results.items():
            report.append(f"  - {r_id}: {result}")
        return "\n".join(report)

class ComplianceChecker:
    """
    Engine to check artifacts against policies.
    """
    def check(self, artifact: Any, policy: GovernancePolicy) -> ComplianceReport:
        results = {}
        all_passed = True
        
        for rule in policy.rules:
            try:
                # The check function returns True if passed, False otherwise
                passed = rule.check_func(artifact)
                if passed:
                    results[rule.id] = "Pass"
                else:
                    results[rule.id] = "Fail"
                    all_passed = False
            except Exception as e:
                results[rule.id] = f"Error: {str(e)}"
                all_passed = False
        
        return ComplianceReport(policy.name, all_passed, results)
