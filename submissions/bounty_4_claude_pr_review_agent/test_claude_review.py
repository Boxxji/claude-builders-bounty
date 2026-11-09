#!/usr/bin/env python3
import unittest
from claude_review import analyze_diff_and_generate_markdown_review


class TestClaudePRReviewAgent(unittest.TestCase):
    def test_pr_review_detects_security_risks_on_pr_1(self) -> None:
        diff_1 = """--- a/auth.py
+++ b/auth.py
@@ -10,2 +10,4 @@
+API_KEY = "sk-live-12345"
+query = f"SELECT * FROM users WHERE name = '{user_input}'"
+subprocess.Popen(cmd, shell=True)
"""
        res = analyze_diff_and_generate_markdown_review(
            repo="org/service-api",
            pr_number=42,
            pr_title="Add user lookup helper",
            diff_text=diff_1,
        )
        self.assertGreaterEqual(res["risks_count"], 3)
        self.assertIn("CHANGES_REQUESTED", res["markdown_review"])
        self.assertIn("## 4. Confidence Score", res["markdown_review"])

    def test_pr_review_approves_clean_diff_on_pr_2(self) -> None:
        diff_2 = """--- a/math_utils.py
+++ b/math_utils.py
@@ -1,2 +1,4 @@
+def clamp_ratio(val: float) -> float:
+    return max(0.0, min(1.0, val))
"""
        res = analyze_diff_and_generate_markdown_review(
            repo="org/quant-core",
            pr_number=108,
            pr_title="Add bounded ratio helper",
            diff_text=diff_2,
        )
        self.assertEqual(res["risks_count"], 0)
        self.assertIn("APPROVED", res["markdown_review"])
        self.assertEqual(res["confidence_label"], "High")


if __name__ == "__main__":
    unittest.main()
