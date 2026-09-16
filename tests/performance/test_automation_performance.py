import subprocess
import sys
import time
import unittest
from pathlib import Path


class AutomationPerformanceTests(unittest.TestCase):

    def test_automation_execution_time(self) -> None:
        project_root = Path(__file__).resolve().parents[2]

        start_time = time.perf_counter()

        result = subprocess.run(
            [
                sys.executable,
                "automation.py",
            ],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )

        elapsed_seconds = time.perf_counter() - start_time

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stderr,
        )

        self.assertLess(
            elapsed_seconds,
            5.0,
            msg=(
                "Automation execution exceeded "
                "the 5-second performance threshold."
            ),
        )

        print(
            f"\nAutomation execution time: "
            f"{elapsed_seconds:.4f} seconds"
        )


if __name__ == "__main__":
    unittest.main()