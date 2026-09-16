import unittest
from unittest.mock import Mock

from src.automation.ticket_analyzer import TicketAnalyzer


class TicketAnalyzerTests(unittest.TestCase):

    def setUp(self) -> None:
        self.repository = Mock()
        self.analyzer = TicketAnalyzer(self.repository)

    def test_empty_ticket_list(self) -> None:
        self.repository.list_all.return_value = []

        result = self.analyzer.analyze()

        self.assertEqual(result["total_tickets"], 0)
        self.assertEqual(result["status_summary"], {})
        self.assertEqual(result["priority_summary"], {})
        self.assertEqual(result["active_tickets"], [])
        self.assertEqual(result["attention_required"], [])
        self.assertEqual(result["unassigned_tickets"], [])

    def test_ticket_analysis(self) -> None:
        ticket_1 = Mock()
        ticket_1.ticket_number = "HD-00001"
        ticket_1.status.value = "OPEN"
        ticket_1.priority.value = "CRITICAL"
        ticket_1.assigned_to = None

        ticket_2 = Mock()
        ticket_2.ticket_number = "HD-00002"
        ticket_2.status.value = "CLOSED"
        ticket_2.priority.value = "HIGH"
        ticket_2.assigned_to = "Support Engineer"

        self.repository.list_all.return_value = [
            ticket_1,
            ticket_2,
        ]

        result = self.analyzer.analyze()

        self.assertEqual(result["total_tickets"], 2)

        self.assertEqual(
            result["status_summary"],
            {
                "OPEN": 1,
                "CLOSED": 1,
            },
        )

        self.assertEqual(
            result["priority_summary"],
            {
                "CRITICAL": 1,
                "HIGH": 1,
            },
        )

        self.assertEqual(
            result["active_tickets"],
            ["HD-00001"],
        )

        self.assertEqual(
            result["attention_required"],
            ["HD-00001"],
        )

        self.assertEqual(
            result["unassigned_tickets"],
            ["HD-00001"],
        )


if __name__ == "__main__":
    unittest.main()