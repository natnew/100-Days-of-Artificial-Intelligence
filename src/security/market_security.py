
from typing import List, Dict, Any
import time

class MarketMonitor:
    """
    Day 87: Market Manipulation Detector.
    Monitors trading logs to detect patterns of 'spoofing', 
    'wash trading', and 'pump and dump' behavior by AI agents.
    """
    def __init__(self, volume_threshold: float = 1000.0):
        self.volume_threshold = volume_threshold
        # Tracks (agent_id) -> list of orders: (price, vol, timestamp, status)
        self.order_history: Dict[str, List[Dict[str, Any]]] = {}

    def log_order(self, agent_id: str, price: float, volume: float, action: str):
        """
        Logs a new order action (PLACE, CANCEL, EXECUTE).
        """
        if agent_id not in self.order_history:
            self.order_history[agent_id] = []
            
        self.order_history[agent_id].append({
            "price": price,
            "volume": volume,
            "action": action,
            "timestamp": time.time()
        })

    def detect_spoofing(self, agent_id: str) -> bool:
        """
        Detects if an agent frequently PLACES high-volume orders 
        and CANCELS them without execution (Spoofing).
        """
        history = self.order_history.get(agent_id, [])
        if len(history) < 5: return False
        
        cancellations = [o for o in history if o["action"] == "CANCEL" and o["volume"] > self.volume_threshold]
        placements = [o for o in history if o["action"] == "PLACE" and o["volume"] > self.volume_threshold]
        
        # If cancellation rate of large orders is > 80%
        if len(placements) > 0 and (len(cancellations) / len(placements)) > 0.8:
            return True
        return False

    def detect_wash_trading(self, agent_id: str) -> bool:
        """
        Detects if an agent is trading with themselves (simulated here by 
        multiple high-speed opposing trades at the same price).
        """
        history = self.order_history.get(agent_id, [])
        if len(history) < 4: return False
        
        # Simple heuristic: fast alternating buy/sell at same price
        opposing_trades = 0
        for i in range(1, len(history)):
            prev, curr = history[i-1], history[i]
            if prev["price"] == curr["price"] and prev["action"] != curr["action"]:
                if (curr["timestamp"] - prev["timestamp"]) < 0.1: # Speed check
                    opposing_trades += 1
                    
        return opposing_trades >= 2

    def audit_agent(self, agent_id: str) -> Dict[str, Any]:
        """Runs all detectors for a specific agent."""
        is_spoofing = self.detect_spoofing(agent_id)
        is_wash = self.detect_wash_trading(agent_id)
        
        return {
            "agent_id": agent_id,
            "suspicious": is_spoofing or is_wash,
            "flags": {
                "spoofing": is_spoofing,
                "wash_trading": is_wash
            }
        }
