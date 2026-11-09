#!/usr/bin/env python3
import unittest
from pathlib import Path


class TestNextJsSqliteClaudeMd(unittest.TestCase):
    def test_all_required_sections_and_rules_present(self) -> None:
        content = (Path(__file__).resolve().parent / "CLAUDE.md").read_text(encoding="utf-8")
        required = [
            "Stack & Pinned Versions",
            "Folder Structure",
            "SQL & Migration Conventions",
            "Development Commands",
            "Component & Data Patterns",
            "What We Don't Do (And Why)",
            "PRAGMA journal_mode = WAL",
            "Next.js 15",
            "0x51E24000948150400166b40d486dB7b3C5b2C5A1",
        ]
        for token in required:
            self.assertIn(token, content, f"Missing required section/rule: {token}")


if __name__ == "__main__":
    unittest.main()
