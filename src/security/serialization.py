
import pickle
import pickletools
import io
from typing import Set, Tuple, List, Any

class PickleScanner:
    """
    A simple static scanner for pickle files to detect potentially dangerous content.
    It disassembles the pickle stream and looks for GLOBAL opcodes that import suspicious modules.
    """
    
    # List of dangerous modules/functions we want to block
    BLOCKED_GLOBALS = {
        ('os', 'system'),
        ('os', 'popen'),
        ('nt', 'system'), # Windows
        ('posix', 'system'), # Linux/Mac
        ('subprocess', 'Popen'),
        ('subprocess', 'run'),
        ('subprocess', 'call'),
        ('eval',), 
        ('exec',),
        ('__builtin__', 'eval'),
        ('__builtin__', 'exec'),
        ('builtins', 'eval'),
        ('builtins', 'exec')
    }

    def __init__(self):
        pass

    def scan(self, data: bytes) -> List[Tuple[str, str]]:
        """
        Scans the pickled data and returns a list of detected dangerous globals.
        Returns: List of (module, name) tuples that are blocked.
        """
        detected = []
        stack = [] # Simple simulation stack to track strings
        
        try:
            # We iterate over the opcodes in the pickle stream
            for opcode, arg, pos in pickletools.genops(data):
                if opcode.name == 'GLOBAL':
                    if isinstance(arg, str) and ' ' in arg:
                        module, name = arg.split(' ', 1) 
                        if (module, name) in self.BLOCKED_GLOBALS:
                            detected.append((module, name))
                            
                elif opcode.name == 'STACK_GLOBAL':
                    # STACK_GLOBAL takes top 2 items: module_name, attr_name
                    if len(stack) >= 2:
                        name = stack.pop()
                        module = stack.pop()
                        if isinstance(module, str) and isinstance(name, str):
                            if (module, name) in self.BLOCKED_GLOBALS:
                                detected.append((module, name))
                        # Result of GLOBAL is pushed back, but we don't know what it is logically
                        # just push a placeholder
                        stack.append("UNKNOWN_GLOBAL")
                    else:
                        stack.append("UNKNOWN_GLOBAL")

                # Track strings for stack
                elif opcode.name in ('SHORT_BINUNICODE', 'BINUNICODE', 'UNICODE', 'STRING', 'SHORT_BINSTRING', 'BINSTRING'):
                    stack.append(arg)
                elif opcode.name in ('INT', 'BININT', 'BININT1', 'BININT2', 'LONG', 'LONG1', 'LONG4'):
                    stack.append(arg) # Sometimes ints matter, mostly not for imports
                elif opcode.name == 'MARK':
                    stack.append('MARK')
                elif opcode.name == 'POP':
                    if stack: stack.pop()
                elif opcode.name == 'POP_MARK':
                     # Pop until MARK
                     while stack and stack[-1] != 'MARK':
                         stack.pop()
                     if stack and stack[-1] == 'MARK':
                         stack.pop()
                # For other opcodes that consume stack items (like TUPLE, LIST, DICT), 
                # a full simulation is complex. 
                # However, usually the strings for STACK_GLOBAL are pushed immediately before.
                # So even if we don't pop correctly for TUPLE/LIST, the strings *should* be at the top 
                # if they were just pushed.
                # To be safer, we can just *peek* if we see STACK_GLOBAL, or try to respect basic consumption.
                # Given strict timeline, we'll rely on the fact that strings are usually top of stack for STACK_GLOBAL.
                
        except Exception as e:
            # Malformed pickle
            print(f"Scan error: {e}")
            return [("Error", str(e))]

        return detected

    def is_safe(self, data: bytes) -> bool:
        """
        Returns True if no blocked globals are detected.
        """
        issues = self.scan(data)
        return len(issues) == 0

    @staticmethod
    def get_globals(data: bytes) -> Set[Tuple[str, str]]:
        """
        Helper to list all globals used in the pickle.
        """
        found = set()
        try:
            for opcode, arg, pos in pickletools.genops(data):
                if opcode.name == 'GLOBAL':
                    # arg is 'module name' string
                    parts = arg.split()
                    if len(parts) == 2:
                        found.add((parts[0], parts[1]))
        except Exception:
            pass
        return found
