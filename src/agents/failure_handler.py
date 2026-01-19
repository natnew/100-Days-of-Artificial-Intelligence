
import time
from typing import Callable, Any, Dict, Type

class FailureHandler:
    """
    Manages robust execution with Retries and Fallbacks.
    """
    def __init__(self, max_retries: int = 3, retry_delay: float = 0.5):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.fallbacks: Dict[Type[Exception], Callable] = {}

    def register_fallback(self, exception_type: Type[Exception], fallback_func: Callable):
        """
        Register a function to call if a specific exception persists after retries.
        """
        self.fallbacks[exception_type] = fallback_func

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute func with retries. If fails, try fallback.
        """
        last_exception = None
        
        # 1. Retry Loop
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                print(f"[FailureHandler] Attempt {attempt + 1} failed: {e}")
                time.sleep(self.retry_delay)
        
        # 2. Fallback execution
        print(f"[FailureHandler] All retries failed for {func.__name__}")
        
        # Check if we have a handler for this exception type
        # We check classes in MRO order to find most specific handler or base handler
        for cls in type(last_exception).mro():
            if cls in self.fallbacks:
                print(f"[FailureHandler] Invoking fallback for {cls.__name__}")
                return self.fallbacks[cls](*args, **kwargs)
        
        # 3. Give up
        print("[FailureHandler] No fallback found. Raising exception.")
        raise last_exception
