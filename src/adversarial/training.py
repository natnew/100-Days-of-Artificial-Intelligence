
from typing import List, Set
from src.adversarial.simulator import AttackSimulator, AttackStrategy
from src.adversarial.defenses import InputSanitizer

class RobustAgent:
    """
    An agent that learns from attacks.
    """
    def __init__(self):
        self.blocklist: Set[str] = set()
        self.sanitizer = InputSanitizer()

    def process(self, prompt: str) -> str:
        # 1. Sanitize
        clean_prompt = self.sanitizer.sanitize(prompt)
        
        # 2. Check Blocklist
        for bad_pattern in self.blocklist:
            if bad_pattern in clean_prompt:
                return "BLOCKED"
                
        # 3. Core Logic
        return f"Processed: {clean_prompt}"

    def update_blocklist(self, new_pattern: str):
        print(f"Adversarial Update: Adding '{new_pattern}' to blocklist.")
        self.blocklist.add(new_pattern)

class DefenseLoop:
    """
    Simulates the Red Team -> Blue Team loop.
    1. Attack (Red)
    2. Check Success
    3. Patch (Blue)
    """
    def __init__(self, agent: RobustAgent, simulator: AttackSimulator):
        self.agent = agent
        self.simulator = simulator

    def run_epoch(self, base_prompt: str):
        print(f"--- Adversarial Epoch for '{base_prompt}' ---")
        
        # 1. Generate Attacks
        results = self.simulator.run_simulation(base_prompt)
        
        # 2. Analyze & Patch
        for res in results:
            response = res['response']
            # If the agent processed it successfully (meaning attack worked/bypass succeeded)
            # We assume "Processed:" indicates success in our mock agent.
            if "Processed:" in response and "sensitive" in res['prompt']: # Mock success condition
                 print(f"Attack Success Detected! Strategy: {res['strategy']}")
                 # 3. Patch: Add specific pattern to blocklist
                 # Simplistic learning: Block the specific attack string
                 self.agent.update_blocklist(res['prompt'])
