#!/usr/bin/env python3
import json
import unittest
from pathlib import Path


class TestN8nWeeklyWorkflow(unittest.TestCase):
    def test_valid_importable_n8n_workflow_schema(self) -> None:
        wf_path = Path(__file__).resolve().parent / "n8n_weekly_claude_dev_summary.json"
        wf = json.loads(wf_path.read_text(encoding="utf-8"))
        self.assertIn("nodes", wf)
        self.assertIn("connections", wf)
        self.assertEqual(len(wf["nodes"]), 6)
        raw_str = json.dumps(wf)
        self.assertIn("claude-sonnet-4-20250514", raw_str)
        self.assertIn("0 17 * * 5", raw_str)


if __name__ == "__main__":
    unittest.main()
