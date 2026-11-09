#!/usr/bin/env python3
import unittest
from changelog_generator import generate_structured_changelog


class TestChangelogGenerator(unittest.TestCase):
    def test_categorizes_into_added_fixed_changed_removed(self) -> None:
        sample_commits = [
            "feat(wallet): bind exclusively to Wallet 1 :: SI_Gemini",
            "fix(rpc): handle Arbitrum EIP-2612 nonce lookup",
            "refactor(dex): query Uniswap v3 slot0 on Arbitrum and Base",
            "remove(legacy): drop deprecated mock account fixtures",
        ]
        res = generate_structured_changelog(sample_commits, version="v3.2.0")
        cats = res["categories"]
        self.assertEqual(len(cats["Added"]), 1)
        self.assertEqual(len(cats["Fixed"]), 1)
        self.assertEqual(len(cats["Changed"]), 1)
        self.assertEqual(len(cats["Removed"]), 1)
        self.assertIn("## Added", res["markdown"])
        self.assertIn("## Fixed", res["markdown"])
        self.assertIn("## Changed", res["markdown"])
        self.assertIn("## Removed", res["markdown"])


if __name__ == "__main__":
    unittest.main()
