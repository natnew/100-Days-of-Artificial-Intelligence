
from dataclasses import dataclass
from typing import List, Any, Callable

@dataclass
class TestScenario:
    name: str
    input_prompt: str
    expected_substring: str # Simple check: does output contain this?
    is_safety_test: bool

@dataclass
class EvaluationResult:
    scenario_name: str
    passed: bool
    actual_output: str
    error: str = ""

@dataclass
class SuiteReport:
    total_tests: int
    passed_tests: int
    safety_violations: int
    results: List[EvaluationResult]

    def summary(self) -> str:
        rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        return (
            f"--- Suite Report ---\n"
            f"Total: {self.total_tests}\n"
            f"Passed: {self.passed_tests} ({rate:.1f}%)\n"
            f"Safety Violations: {self.safety_violations}\n"
        )

class AgentEvaluationHarness:
    """
    Runs a suite of scenarios against an agent (any object with a .run(prompt) method).
    """
    def __init__(self):
        pass

    def run_suite(self, agent: Any, scenarios: List[TestScenario]) -> SuiteReport:
        results = []
        passed = 0
        safety_violations = 0
        
        for scenario in scenarios:
            try:
                # 1. Run Agent
                response = agent.run(scenario.input_prompt)
                
                # 2. Check Result
                is_pass = scenario.expected_substring.lower() in response.lower()
                
                if is_pass:
                    passed += 1
                elif scenario.is_safety_test:
                    # If a safety test failed (did NOT contain refusal), it's a violation
                    safety_violations += 1
                    
                results.append(EvaluationResult(
                    scenario_name=scenario.name,
                    passed=is_pass,
                    actual_output=response
                ))
                
            except Exception as e:
                # Harness error or agent crash
                results.append(EvaluationResult(
                    scenario_name=scenario.name,
                    passed=False,
                    actual_output="ERROR",
                    error=str(e)
                ))
                
        return SuiteReport(
            total_tests=len(scenarios),
            passed_tests=passed,
            safety_violations=safety_violations,
            results=results
        )
