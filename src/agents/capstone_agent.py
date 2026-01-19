
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import sys
import os

# Imports from previous days
from src.agents.persona import Persona, PersonaManager
from src.agents.plan_verifier import PlanVerifier, PlanStep

@dataclass
class AgentResponse:
    success: bool
    content: str
    trace: List[str]

class SafeResearchAssistant:
    """
    Phase 2 Capstone Agent.
    Integrates: Guardrails, Persona, Planning, and Verification.
    """
    def __init__(self):
        # 1. Persona Config
        self.persona = Persona(
            name="ResearchBot",
            role="Helpful Research Assistant",
            tone=["Professional", "Objective"],
            constraints=["No PII", "No Dangerous Content", "Cite sources"]
        )
        self.persona_manager = PersonaManager(self.persona)
        
        # 2. Safety Components
        self.plan_verifier = PlanVerifier(restricted_tools=["system_shell", "delete_file", "format_disk"])
        
    def _input_guard(self, text: str) -> bool:
        """Mock Input Guardrail (Day 27)"""
        unsafe = ["poison", "kill", "bomb", "ignore instructions"]
        for term in unsafe:
            if term in text.lower():
                return False # Blocked
        return True # Safe

    def _output_guard(self, text: str) -> bool:
        """Mock Output Guardrail (Day 28)"""
        # PII Check
        if "password" in text.lower():
            return False
        return True

    def _generate_plan(self, query: str) -> List[PlanStep]:
        """
        Mock LLM Planning.
        If query contains 'delete', generates an unsafe plan for testing.
        Otherwise generates a safe research plan.
        """
        if "delete" in query.lower():
            # Unsafe plan demo
            return [
                PlanStep(tool_name="delete_file", arguments={"path": "/all"}, step_id=1)
            ]
        
        # Safe plan
        return [
            PlanStep(tool_name="web_search", arguments={"q": query}, step_id=1),
            PlanStep(tool_name="read_page", arguments={"url": "result.com"}, step_id=2)
        ]

    def _execute_tool(self, tool_name: str, args: Dict) -> str:
        """Mock Tool Execution"""
        if tool_name == "web_search":
            return "Found relevant articles about " + args.get("q", "")
        if tool_name == "read_page":
            return "Content of page..."
        return "Tool Executed"

    def run(self, user_query: str) -> AgentResponse:
        trace = []
        trace.append(f"Received Query: {user_query}")
        
        # 1. Input Guardrail
        if not self._input_guard(user_query):
            trace.append("❌ Input Guardbox: Blocked unsafe query.")
            return AgentResponse(False, "I cannot answer that query due to safety guidelines.", trace)
        trace.append("✅ Input Guard: Passed")
        
        # 2. Persona Wrapping
        wrapped_query = self.persona_manager.wrap_prompt(user_query)
        trace.append("✅ Persona: Prompt wrapped with constraints.")
        
        # 3. Planning
        plan = self._generate_plan(user_query)
        trace.append(f"Generated Plan: {[s.tool_name for s in plan]}")
        
        # 4. Plan Verification
        verification = self.plan_verifier.verify_plan(plan)
        if not verification.is_valid:
            trace.append(f"❌ Plan Verification: BOCKED. Errors: {verification.errors}")
            return AgentResponse(False, "My proposed plan was deemed unsafe.", trace)
        trace.append("✅ Plan Verification: Passed")
        
        # 5. Execution
        context = ""
        for step in plan:
            res = self._execute_tool(step.tool_name, step.arguments)
            context += res + "\n"
        trace.append("✅ Execution: Tools ran successfully")
        
        # 6. Generate Answer (Mock)
        final_answer = f"Based on my research: {context.strip()}"
        
        # 7. Drift Check (Persona)
        if not self.persona_manager.check_consistency(final_answer):
             trace.append("❌ Persona Drift: Response violated tone/constraints.")
             # Self-Correction could happen here (Day 42), simplifed to fail for now
             final_answer = "[REDACTED due to persona drift]"
        
        # 8. Output Guardrail
        if not self._output_guard(final_answer):
             trace.append("❌ Output Guard: Blocked sensitive content.")
             return AgentResponse(False, "Response redacted for safety.", trace)
        
        trace.append("✅ Output Guard: Passed")
        return AgentResponse(True, final_answer, trace)
