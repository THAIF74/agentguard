import yaml
from pathlib import Path
from typing import Any


class PolicyViolation(Exception):
    pass


class PolicyEngine:
    def __init__(self, path: str = "policies.yaml"):
        self.rules = yaml.safe_load(Path(path).read_text())["rules"]

    def check(self, tool: str, args: dict[str, Any]) -> None:
        for rule in self.rules:
            if not self._matches(rule, tool):
                continue
            if self._denied(rule, args):
                raise PolicyViolation(f"{rule['name']}: {rule['description']}")

    def _matches(self, rule, tool):
        return rule.get("match", {}).get("tool") == tool

    def _denied(self, rule, args) -> bool:
        deny = rule.get("deny_if", {})
        if "arg_contains" in deny:
            for needle in deny["arg_contains"]:
                for v in args.values():
                    if needle in str(v):
                        return True
        if "arg_greater_than" in deny:
            spec = deny["arg_greater_than"]
            if args.get(spec["field"], 0) > spec["value"]:
                return True
        return False