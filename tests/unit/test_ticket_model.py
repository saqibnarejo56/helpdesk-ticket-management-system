import unittest
from datetime import datetime, timezone

from src.models.ticket import (
    Ticket,
    TicketCategory,
    TicketPriority,
    TicketStatus,
)


class TicketModelTests(unittest.TestCase):

    @staticmethod
    def create_ticket() -> Ticket:
        return Ticket(
            ticket_number="HD-00001",
            title="Laptop not starting",
            description="Laptop does not power on.",
            category=TicketCategory.HARDWARE,
            requester_name="Test User",
            requester_email="test@example.com",
        )

    def test_default_priority_is_medium(self) -> None:
        ticket = self.create_ticket()

        self.assertEqual(
            ticket.priority,
            TicketPriority.MEDIUM,
        )

    def test_default_status_is_open(self) -> None:
        ticket = self.create_ticket()

        self.assertEqual(
            ticket.status,
            TicketStatus.OPEN,
        )

    def test_new_ticket_has_no_database_id(self) -> None:
        ticket = self.create_ticket()

        self.assertIsNone(
            ticket.id
        )

    def test_timestamps_are_timezone_aware(self) -> None:
        ticket = self.create_ticket()

        self.assertIsNotNone(
            ticket.created_at.tzinfo
        )

        self.assertIsNotNone(
            ticket.updated_at.tzinfo
        )

        self.assertEqual(
            ticket.created_at.utcoffset(),
            timezone.utc.utcoffset(
                ticket.created_at
            ),
        )

    def test_touch_updates_timestamp(self) -> None:
        ticket = self.create_ticket()

        old_updated_at = ticket.updated_at

        ticket.touch()

        self.assertGreaterEqual(
            ticket.updated_at,
            old_updated_at,
        )

    def test_to_dict_returns_serializable_values(self) -> None:
        ticket = self.create_ticket()

        ticket.id = 1
        ticket.priority = TicketPriority.HIGH
        ticket.status = TicketStatus.IN_PROGRESS

        data = ticket.to_dict()

        self.assertEqual(
            data["id"],
            1,
        )

        self.assertEqual(
            data["ticket_number"],
            "HD-00001",
        )

        self.assertEqual(
            data["category"],
            "Hardware",
        )

        self.assertEqual(
            data["priority"],
            "HIGH",
        )

        self.assertEqual(
            data["status"],
            "IN_PROGRESS",
        )

        self.assertIsInstance(
            data["created_at"],
            str,
        )

        self.assertIsInstance(
            data["updated_at"],
            str,
        )

        self.assertIsNone(
            data["resolved_at"]
        )

        self.assertIsNone(
            data["closed_at"]
        )


if __name__ == "__main__":
    unittest.main()
