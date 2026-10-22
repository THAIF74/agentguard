from functools import wraps
from .policy import PolicyEngine, PolicyViolation
from .audit import AuditLog
from .state import state

class Guard:
    def __init__(self, engine: PolicyEngine, audit: AuditLog | None = None):
        self.engine = engine
        self.audit = audit or AuditLog()

    def wrap(self, tool_name: str, fn):
        @wraps(fn)
        def wrapped(**kwargs):
            # 1. Check if FROZEN
            if state.frozen:
                reason = "System is FROZEN. Action blocked."
                self.audit.append(tool_name, kwargs, allowed=False, reason=reason)
                print(f"🧊 BLOCKED: {reason}")
                return {"blocked": True, "reason": reason}

            # 2. Check Policies
            try:
                self.engine.check(tool_name, kwargs)
            except PolicyViolation as e:
                self.audit.append(tool_name, kwargs, allowed=False, reason=str(e))
                print(f"🚫 BLOCKED: {e}")
                return {"blocked": True, "reason": str(e)}

            # 3. Allowed
            self.audit.append(tool_name, kwargs, allowed=True, reason=None)
            return fn(**kwargs)
        return wrapped
