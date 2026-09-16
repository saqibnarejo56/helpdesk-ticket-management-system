import csv
import json
import tempfile
import unittest
from pathlib import Path

from src.automation.report_generator import ReportGenerator


class ReportGeneratorTests(unittest.TestCase):

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.output_directory = Path(
            self.temporary_directory.name
        )
        self.generator = ReportGenerator(
            self.output_directory
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_generate_json_report(self) -> None:
        analysis = {
            "total_tickets": 2,
            "status_summary": {
                "RESOLVED": 1,
                "CLOSED": 1,
            },
            "priority_summary": {
                "HIGH": 2,
            },
            "active_tickets": [],
            "attention_required": [
                "HD-00002",
            ],
            "unassigned_tickets": [
                "HD-00002",
            ],
        }

        output_path = self.generator.generate_json_report(
            analysis
        )

        self.assertTrue(output_path.exists())

        with output_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            generated_data = json.load(file)

        self.assertEqual(
            generated_data,
            analysis,
        )

    def test_generate_active_tickets_csv(self) -> None:
        analysis = {
            "active_tickets": [
                "HD-00003",
                "HD-00004",
            ],
        }

        output_path = (
            self.generator.generate_active_tickets_report(
                analysis
            )
        )

        self.assertTrue(output_path.exists())

        with output_path.open(
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            rows = list(csv.reader(file))

        self.assertEqual(
            rows,
            [
                ["ticket_number"],
                ["HD-00003"],
                ["HD-00004"],
            ],
        )

    def test_generate_empty_active_tickets_csv(
        self,
    ) -> None:
        output_path = (
            self.generator.generate_active_tickets_report(
                {
                    "active_tickets": [],
                }
            )
        )

        self.assertTrue(output_path.exists())

        with output_path.open(
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            rows = list(csv.reader(file))

        self.assertEqual(
            rows,
            [
                ["ticket_number"],
            ],
        )


if __name__ == "__main__":
    unittest.main()