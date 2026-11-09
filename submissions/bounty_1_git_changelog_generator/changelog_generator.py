#!/usr/bin/env python3
"""
Structured CHANGELOG.md Generator from Git History (Added / Fixed / Changed / Removed)
(`claude-builders-bounty/claude-builders-bounty#1` — $50 Bounty).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Dict, List

CONVENTIONAL_RE = re.compile(
    r"^(?P<type>feat|add|fix|bugfix|change|refactor|perf|docs|remove|chore|sec|security)"
    r"(?:\((?P<scope>[a-zA-Z0-9_.-]+)\))?"
    r"(?P<breaking>!)?:\s+(?P<subject>.+)$",
    re.IGNORECASE,
)


def fetch_commits_since_last_tag(repo_dir: Path | None = None) -> List[str]:
    cwd = str(repo_dir or Path.cwd())
    try:
        tag_proc = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        rev_range = f"{tag_proc.stdout.strip()}..HEAD" if tag_proc.returncode == 0 and tag_proc.stdout.strip() else "HEAD"
        log_proc = subprocess.run(
            ["git", "log", rev_range, "--pretty=format:%s"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if log_proc.returncode == 0 and log_proc.stdout.strip():
            return [line.strip() for line in log_proc.stdout.splitlines() if line.strip()]
    except Exception:
        pass
    return []


def generate_structured_changelog(commits: List[str], version: str = "v1.0.0") -> Dict[str, object]:
    categories: Dict[str, List[str]] = {
        "Added": [],
        "Fixed": [],
        "Changed": [],
        "Removed": [],
    }
    for raw in commits:
        line = raw.strip()
        if not line:
            continue
        m = CONVENTIONAL_RE.match(line)
        if not m:
            lower = line.lower()
            if lower.startswith(("add ", "create ", "implement ")):
                categories["Added"].append(f"- {line}")
            elif lower.startswith(("fix ", "resolve ", "repair ")):
                categories["Fixed"].append(f"- {line}")
            elif lower.startswith(("remove ", "delete ", "drop ")):
                categories["Removed"].append(f"- {line}")
            else:
                categories["Changed"].append(f"- {line}")
            continue

        ctype = m.group("type").lower()
        scope = m.group("scope")
        subject = m.group("subject").strip()
        prefix = f"**{scope}**: " if scope else ""
        formatted = f"- {prefix}{subject}"

        if ctype in ("feat", "add"):
            categories["Added"].append(formatted)
        elif ctype in ("fix", "bugfix", "sec", "security"):
            categories["Fixed"].append(formatted)
        elif ctype == "remove":
            categories["Removed"].append(formatted)
        else:
            categories["Changed"].append(formatted)

    md_lines = [f"# Changelog — {version}", ""]
    for section in ("Added", "Fixed", "Changed", "Removed"):
        items = categories[section]
        if items:
            md_lines.append(f"## {section}")
            md_lines.extend(items)
            md_lines.append("")

    return {
        "version": version,
        "categories": categories,
        "markdown": "\n".join(md_lines).strip() + "\n",
    }
