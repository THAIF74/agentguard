import argparse
from .audit import AuditLog


def cmd_list(args):
    log = AuditLog()
    for e in log.entries(limit=args.limit):
        mark = "OK " if e["allowed"] else "BLK"
        print(f"[{e['id']:3}] {mark} {e['tool']:15} {e['args'][:60]}")
        if not e["allowed"]:
            print(f"      reason: {e['reason']}")


def cmd_verify(args):
    log = AuditLog()
    ok, msg, broken = log.verify()
    print(("✅ " if ok else "❌ ") + msg)


def main():
    p = argparse.ArgumentParser(prog="agentguard")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list")
    pl.add_argument("--limit", type=int, default=50)
    pl.set_defaults(fn=cmd_list)

    pv = sub.add_parser("verify")
    pv.set_defaults(fn=cmd_verify)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()