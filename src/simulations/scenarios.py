from .bad_agents import StubbornAgent, DriftingAgent, PrematureCloserAgent, RoleBreakerAgent
from ..orchestration.schema import Message, AgentRole, TaskSpec

class SimulationRunner:
    def run_interaction(self, agent_a, agent_b, turns=3):
        history = []
        print(f"--- Simulating {agent_a.name} vs {agent_b.name} ---")
        for i in range(turns):
            # Agent A turn
            msg_a = agent_a.generate(history)
            print(f"{agent_a.name}: {msg_a}")
            history.append(Message(source=agent_a.name, role=agent_a.role, content=msg_a))
            
            # Simple check for termination
            if "TASK_DONE" in msg_a:
                return history

            # Agent B turn
            msg_b = agent_b.generate(history)
            print(f"{agent_b.name}: {msg_b}")
            history.append(Message(source=agent_b.name, role=agent_b.role, content=msg_b))
            
            if "TASK_DONE" in msg_b:
                return history
        
        return history

def simulate_fc1_drift():
    print("\n=== Simulation FC1: Spec Drift ===")
    agent = DriftingAgent("Worker", AgentRole.PRIMARY)
    other = StubbornAgent("User", AgentRole.OBSERVER) # Dummy
    runner = SimulationRunner()
    history = runner.run_interaction(agent, other, turns=3)
    
    # Verification logic: Did it drift?
    last_msg = history[-1].content
    if "weather" in last_msg:
        print("[FAIL] Agent drifted to irrelevant topic.")
    else:
        print("[PASS] Agent stayed on topic.")

def simulate_fc2_loop():
    print("\n=== Simulation FC2: Infinite Loop ===")
    agent_a = StubbornAgent("BotA", AgentRole.PRIMARY)
    agent_b = StubbornAgent("BotB", AgentRole.PRIMARY) # Two stubborn agents
    runner = SimulationRunner()
    history = runner.run_interaction(agent_a, agent_b, turns=3)
    
    # Check for repetition
    contents = [m.content for m in history]
    if len(set(contents)) < len(contents) * 0.6: # High repetition
        print("[FAIL] Agents entered a repetitive loop.")

def simulate_fc3_premature_closure():
    print("\n=== Simulation FC3: False Success ===")
    start_msg = Message(source="User", role=AgentRole.OBSERVER, content="Verify this buggy code.")
    verifier = PrematureCloserAgent("LazyVerifier", AgentRole.REVIEWER)
    
    response = verifier.generate([start_msg])
    print(f"Verifier said: {response}")
    
    if "TASK_DONE" in response and "successful" in response:
        print("[FAIL] Verifier approved without actually running checks (False Positive).")

if __name__ == "__main__":
    simulate_fc1_drift()
    simulate_fc2_loop()
    simulate_fc3_premature_closure()
