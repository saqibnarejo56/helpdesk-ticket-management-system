import json
import tempfile
import unittest
from pathlib import Path

from src.automation.alert_report import AlertReportGenerator
from src.automation.report_generator import ReportGenerator
from src.automation.ticket_analyzer import TicketAnalyzer
from src.database.connection import DatabaseConnection
from src.repositories.ticket_repository import TicketRepository


class AutomationIntegrationTests(unittest.TestCase):

    def test_complete_automation_report_flow(self) -> None:
        database = DatabaseConnection(
            Path("data/helpdesk.db")
        )

        repository = TicketRepository(database)
        analyzer = TicketAnalyzer(repository)

        analysis = analyzer.analyze()

        with tempfile.TemporaryDirectory() as temporary_directory:
            reports_directory = Path(temporary_directory)

            report_generator = ReportGenerator(
                reports_directory
            )

            alert_generator = AlertReportGenerator(
                reports_directory
            )

            json_path = report_generator.generate_json_report(
                analysis
            )

            csv_path = (
                report_generator.generate_active_tickets_report(
                    analysis
                )
            )

            alert_path = alert_generator.generate(
                analysis
            )

            self.assertTrue(json_path.exists())
            self.assertTrue(csv_path.exists())
            self.assertTrue(alert_path.exists())

            with json_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                summary = json.load(file)

            with alert_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                alerts = json.load(file)

            self.assertEqual(
                summary["total_tickets"],
                len(repository.list_all()),
            )

            self.assertEqual(
                summary["attention_required"],
                alerts["attention_required"],
            )

            self.assertEqual(
                summary["unassigned_tickets"],
                alerts["unassigned_tickets"],
            )

            self.assertEqual(
                summary["active_tickets"],
                alerts["active_tickets"],
            )


if __name__ == "__main__":
    unittest.main()