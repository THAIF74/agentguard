from functools import wraps
from .policy import PolicyEngine, PolicyViolation


class Guard:
    def __init__(self, engine: PolicyEngine):
        self.engine = engine

    def wrap(self, tool_name: str, fn):
        @wraps(fn)
        def wrapped(**kwargs):
            try:
                self.engine.check(tool_name, kwargs)
            except PolicyViolation as e:
                print(f"BLOCKED: {e}")
                return {"blocked": True, "reason": str(e)}
            return fn(**kwargs)
        return wrapped