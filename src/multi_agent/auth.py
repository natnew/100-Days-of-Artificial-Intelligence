
import hashlib
import hmac
import base64
import time
from typing import Dict

class Authenticator:
    """
    Simulates a cryptographic authentication system for agents.
    Uses HMAC for signatures and mock tokens.
    """
    def __init__(self, secret_key: str = "master_secret_key"):
        self.secret_key = secret_key.encode()
        self.issued_tokens: Dict[str, str] = {}

    def issue_token(self, agent_id: str, expiry_seconds: int = 3600) -> str:
        """
        Issues a time-bound token for an Agent ID.
        Format: agent_id|expiry|signature
        """
        expiry = int(time.time()) + expiry_seconds
        payload = f"{agent_id}|{expiry}"
        signature = self._sign(payload)
        token = f"{payload}|{signature}"
        return token

    def verify_token(self, token: str, expected_agent_id: str) -> bool:
        """
        Verifies:
        1. Integrity (Signature matches)
        2. Expiry (Not expired)
        3. Identity (Token belongs to expected_agent_id)
        """
        try:
            parts = token.split('|')
            if len(parts) != 3:
                return False
            
            agent_id, expiry_str, signature = parts
            expiry = int(expiry_str)
            
            # 1. Identity Check
            if agent_id != expected_agent_id:
                return False # Token belongs to someone else
            
            # 2. Integrity Check
            payload = f"{agent_id}|{expiry}"
            expected_sig = self._sign(payload)
            if not hmac.compare_digest(signature, expected_sig):
                return False # Tampered
                
            # 3. Expiry Check
            if time.time() > expiry:
                return False # Expired
                
            return True
            
        except ValueError:
            return False

    def sign_message(self, content: str) -> str:
        """
        Signs message content to prevent tampering during transit.
        """
        return self._sign(content)

    def verify_signature(self, content: str, signature: str) -> bool:
        """
        Verifies content integrity.
        """
        expected = self._sign(content)
        return hmac.compare_digest(signature, expected)

    def _sign(self, data: str) -> str:
        return hmac.new(self.secret_key, data.encode(), hashlib.sha256).hexdigest()
