from agentguard.policy import PolicyEngine
from agentguard.interceptor import Guard


def shell(cmd: str):
    return f"ran: {cmd}"


def make_payment(amount: int):
    return f"paid ${amount}"


engine = PolicyEngine()
guard = Guard(engine)

safe_shell = guard.wrap("shell", shell)
safe_pay = guard.wrap("make_payment", make_payment)

print(safe_shell(cmd="ls"))
print(safe_shell(cmd="rm -rf /"))
print(safe_pay(amount=50))
print(safe_pay(amount=5000))    