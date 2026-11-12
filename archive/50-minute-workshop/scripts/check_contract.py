"""Offline domain gate used by CI. It never claims to run an LLM or Azure."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "github-copilot-invocations"))
from volt.domain import recall_notices


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=["baseline", "improved"], default="improved")
    args = parser.parse_args()
    status = recall_notices("VC-C65", None, args.variant)["status"]
    passed = status == "needs_batch"
    print(json.dumps({"mode": "offline-tool-contract", "variant": args.variant,
                      "expected": "needs_batch", "actual": status, "passed": passed}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
