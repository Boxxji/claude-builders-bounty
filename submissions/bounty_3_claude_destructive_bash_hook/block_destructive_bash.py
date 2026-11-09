#!/usr/bin/env python3
"""
Claude Code Pre-Tool-Use Security Hook: Blocks Destructive Bash Commands
(`claude-builders-bounty/claude-builders-bounty#3` — $100 Bounty).
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

DESTRUCTIVE_PATTERNS: List[Tuple[str, re.Pattern[str]]] = [
    ("Recursive forced deletion (rm -rf / rm -fr)", re.compile(r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|--recursive\s+--force|-[a-zA-Z]*f[a-zA-Z]*r)\b", re.IGNORECASE)),
    ("SQL DROP TABLE / DROP DATABASE", re.compile(r"\bDROP\s+(TABLE|DATABASE|SCHEMA)\b", re.IGNORECASE)),
    ("SQL TRUNCATE TABLE", re.compile(r"\bTRUNCATE\s+(TABLE\b|[a-zA-Z0-9_.]+)", re.IGNORECASE)),
    ("Unbounded SQL DELETE FROM without WHERE", re.compile(r"\bDELETE\s+FROM\s+[a-zA-Z0-9_.]+\s*(;|$|'|\")", re.IGNORECASE)),
    ("Git force push (git push --force / -f)", re.compile(r"\bgit\s+push\b.*(\s--force\b|\s-f\b)", re.IGNORECASE)),
    ("Filesystem format / raw disk overwrite (mkfs / dd)", re.compile(r"\b(mkfs\.|dd\s+if=)", re.IGNORECASE)),
]


def evaluate_bash_command(
    command: str,
    log_file: Path | None = None,
    project_path: str | None = None,
) -> Dict[str, Any]:
    proj = project_path or os.getcwd()
    for reason, pattern in DESTRUCTIVE_PATTERNS:
        if pattern.search(command):
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": "BLOCKED",
                "reason": reason,
                "attempted_command": command,
                "project_path": proj,
            }
            target_log = log_file or (Path.home() / ".claude" / "hooks" / "blocked.log")
            target_log.parent.mkdir(parents=True, exist_ok=True)
            with target_log.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry) + "\n")
            return {"allowed": False, "reason": reason, "log_path": str(target_log), "entry": entry}
    return {"allowed": True, "reason": "Command passed Zero-Trust destructive check"}


def main() -> int:
    raw = sys.stdin.read().strip()
    cmd = raw
    if raw.startswith("{"):
        try:
            payload = json.loads(raw)
            cmd = payload.get("tool_input", {}).get("command", raw)
        except Exception:
            pass
    verdict = evaluate_bash_command(cmd)
    if not verdict["allowed"]:
        sys.stderr.write(
            f"[CLAUDE CODE HOOK BLOCKED] Destructive command intercepted ({verdict['reason']}): `{cmd}`\n"
            f"Logged to {verdict['log_path']}\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
