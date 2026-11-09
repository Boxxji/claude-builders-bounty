#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path
from block_destructive_bash import evaluate_bash_command


class TestDestructiveBashHook(unittest.TestCase):
    def test_blocks_destructive_commands_and_logs_project_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_file = Path(tmp) / "blocked.log"
            dangerous = [
                "rm -rf /var/www/html",
                "psql -c 'DROP TABLE users;'",
                "mysql -e 'TRUNCATE TABLE orders;'",
                "sqlite3 app.db 'DELETE FROM accounts;'",
                "git push --force origin main",
            ]
            for cmd in dangerous:
                res = evaluate_bash_command(cmd, log_file=log_file, project_path="/srv/app")
                self.assertFalse(res["allowed"], f"Failed to block: {cmd}")
            lines = log_file.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), len(dangerous))
            first = json.loads(lines[0])
            self.assertEqual(first["project_path"], "/srv/app")
            self.assertIn("timestamp", first)
            self.assertIn("attempted_command", first)

    def test_allows_safe_commands(self) -> None:
        safe = [
            "ls -la /home/antigravity",
            "git push origin feature/safe-branch",
            "sqlite3 app.db 'DELETE FROM sessions WHERE expired = 1;'",
            "python3 -m unittest discover",
        ]
        for cmd in safe:
            res = evaluate_bash_command(cmd)
            self.assertTrue(res["allowed"], f"Falsely blocked safe command: {cmd}")


if __name__ == "__main__":
    unittest.main()
