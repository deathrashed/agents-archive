"""Exercise physical traversal and partial evidence without touching user data."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "inventory", Path(__file__).resolve().parents[1] / "scripts" / "inventory.py")
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class InventoryTests(unittest.TestCase):
    def test_external_link_is_not_traversed(self):
        with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as target:
            external = Path(target)
            (external / "unique.bin").write_bytes(b"x" * 65536)
            link = Path(source) / "linked"
            link.symlink_to(external, target_is_directory=True)
            skipped = inventory.inventory(str(link), 1)
            self.assertTrue(skipped["target_exists"])
            self.assertIn("skipped", skipped)
            result = inventory.inventory(source, 1)
            self.assertTrue(result["complete"])
            self.assertEqual(len(result["symlinks"]), 1)
            self.assertFalse(any("unique.bin" in row["path"] for row in result["entries"]))
            self.assertLess(result["entries"][0]["allocated_bytes"], 65536)

    def test_timeout_preserves_evidence(self):
        with tempfile.TemporaryDirectory() as root:
            error = subprocess.TimeoutExpired("du", 1, output=b"8\t/tmp/child\n", stderr=b"partial\n")
            with patch.object(inventory.subprocess, "run", side_effect=error):
                result = inventory.inventory(root, 1, 1)
            self.assertFalse(result["complete"])
            self.assertTrue(result["timed_out"])
            self.assertEqual(result["entries"][0]["allocated_bytes"], 8192)
            self.assertEqual(result["errors"], ["partial"])

    def test_permission_failure_is_incomplete(self):
        with tempfile.TemporaryDirectory() as root:
            proc = subprocess.CompletedProcess("du", 1, "4\t/tmp/visible\n", "Permission denied\n")
            with patch.object(inventory.subprocess, "run", return_value=proc):
                result = inventory.inventory(root, 1)
            self.assertFalse(result["complete"])
            self.assertEqual(len(result["entries"]), 1)
            self.assertTrue(result["errors"])

    def test_missing_root_reports_error(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertIn("error", inventory.inventory(str(Path(root) / "absent"), 1))


if __name__ == "__main__":
    unittest.main()
