import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("presenter", ROOT / "scripts" / "demo.py")
presenter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(presenter)


class PresenterTests(unittest.TestCase):
    def test_empty_dataset_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.jsonl"
            path.write_text("")
            with self.assertRaises(ValueError):
                presenter.read_cases([path])

    def test_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicates.jsonl"
            path.write_text('{"id":"one"}\n{"id":"one"}\n')
            with self.assertRaises(ValueError):
                presenter.read_cases([path])

    def test_local_target_is_loopback_only(self):
        with self.assertRaises(ValueError):
            presenter.invoke("hello", "https://example.com")

    def test_offline_results_cannot_authorize_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps({"mode": "offline-tool-contract", "gate_passed": True}))
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "release.py"),
                                     "--report", str(path), "--version", "1",
                                     "--out", str(Path(tmp) / "release.json")],
                                    capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertFalse((Path(tmp) / "release.json").exists())

    def test_feedback_requires_live_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "fixture.json"
            source.write_text(json.dumps({"mode": "offline-tool-contract"}))
            destination = Path(tmp) / "reviewed.jsonl"
            result = subprocess.run([
                sys.executable, str(ROOT / "scripts" / "demo.py"), "feedback",
                "--trace", str(source), "--id", "case", "--query", "question",
                "--expected-decision", "unknown", "--expected-behavior", "Do not guess",
                "--reviewer", "test", "--approve", "--out", str(destination),
            ], capture_output=True, text=True)
            self.assertEqual(2, result.returncode)
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
