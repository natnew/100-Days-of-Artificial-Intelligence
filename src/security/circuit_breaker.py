
from typing import List, Dict, Optional
import time

class TradingCircuitBreaker:
    """
    Day 88: Flash Crash Safeguards.
    Implements volatility-based circuit breakers and 
    liquidation dampeners to prevent AI-driven flash crashes.
    """
    def __init__(self, 
                 max_drawdown_pct: float = 0.05, 
                 window_seconds: int = 60,
                 cooldown_seconds: int = 300):
        self.max_drawdown_pct = max_drawdown_pct
        self.window_seconds = window_seconds
        self.cooldown_seconds = cooldown_seconds
        
        # (asset) -> list of (price, timestamp)
        self.price_history: Dict[str, List[tuple]] = {}
        # (asset) -> halt_until_timestamp
        self.halts: Dict[str, float] = {}

    def update_price(self, asset: str, price: float):
        """Logs a new price and checks for volatility triggers."""
        if asset not in self.price_history:
            self.price_history[asset] = []
            
        now = time.time()
        self.price_history[asset].append((price, now))
        
        # Cleanup old data
        self.price_history[asset] = [p for p in self.price_history[asset] if (now - p[1]) <= self.window_seconds]
        
        # Check for crash
        if len(self.price_history[asset]) > 1:
            prices = [p[0] for p in self.price_history[asset]]
            max_p = max(prices)
            min_p = min(prices)
            drawdown = (max_p - min_p) / max_p
            
            if drawdown >= self.max_drawdown_pct:
                self.halts[asset] = now + self.cooldown_seconds
                print(f"[CIRCUIT BREAKER] Flash crash detected in {asset}! Halting all trades for {self.cooldown_seconds}s.")

    def can_trade(self, asset: str) -> bool:
        """Checks if the asset is currently under a halt."""
        now = time.time()
        halt_until = self.halts.get(asset, 0)
        return now > halt_until

    def get_status(self, asset: str) -> str:
        if self.can_trade(asset):
            return "ACTIVE"
        return f"HALTED (until {round(self.halts[asset] - time.time())}s remaining)"
