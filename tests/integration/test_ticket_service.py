import tempfile
import unittest
from pathlib import Path

from src.database.connection import DatabaseConnection
from src.database.schema import DatabaseSchema
from src.exceptions.exceptions import (
    InvalidStatusTransitionError,
    ValidationError,
)
from src.models.ticket import (
    TicketCategory,
    TicketPriority,
    TicketStatus,
)
from src.repositories.ticket_history_repository import (
    TicketHistoryRepository,
)
from src.repositories.ticket_repository import TicketRepository
from src.services.ticket_service import TicketService


class TicketServiceTests(unittest.TestCase):

    def setUp(self) -> None:
        temp_file = tempfile.NamedTemporaryFile(
            suffix=".db",
            delete=False,
        )
        temp_file.close()

        self.database_path = Path(temp_file.name)

        database = DatabaseConnection(
            self.database_path
        )

        schema = DatabaseSchema(
            database
        )
        schema.create()

        ticket_repository = TicketRepository(
            database
        )

        history_repository = TicketHistoryRepository(
            database
        )

        self.service = TicketService(
            ticket_repository,
            history_repository,
        )

    def tearDown(self) -> None:
        self.database_path.unlink(
            missing_ok=True
        )

    def create_ticket(self):
        return self.service.create_ticket(
            title="Laptop not starting",
            description=(
                "Laptop does not power on after "
                "pressing the power button."
            ),
            category=TicketCategory.HARDWARE,
            requester_name="Test User",
            requester_email="test@example.com",
        )

    def test_create_ticket_and_history(self) -> None:
        ticket = self.create_ticket()

        self.assertIsNotNone(
            ticket.id
        )

        self.assertEqual(
            ticket.ticket_number,
            "HD-00001",
        )

        self.assertEqual(
            ticket.status,
            TicketStatus.OPEN,
        )

        history = self.service.get_ticket_history(
            ticket.ticket_number
        )

        self.assertEqual(
            len(history),
            1,
        )

        self.assertEqual(
            history[0]["action"],
            "CREATED",
        )

    def test_assign_ticket(self) -> None:
        ticket = self.create_ticket()

        updated = self.service.assign_ticket(
            ticket.ticket_number,
            "Support Engineer",
        )

        self.assertEqual(
            updated.assigned_to,
            "Support Engineer",
        )

        history = self.service.get_ticket_history(
            ticket.ticket_number
        )

        self.assertEqual(
            history[-1]["action"],
            "ASSIGNED",
        )

    def test_change_priority(self) -> None:
        ticket = self.create_ticket()

        updated = self.service.change_priority(
            ticket.ticket_number,
            TicketPriority.HIGH,
        )

        self.assertEqual(
            updated.priority,
            TicketPriority.HIGH,
        )

        history = self.service.get_ticket_history(
            ticket.ticket_number
        )

        self.assertEqual(
            history[-1]["action"],
            "PRIORITY_CHANGED",
        )

    def test_update_ticket_details(self) -> None:
        ticket = self.create_ticket()

        updated = self.service.update_ticket_details(
            ticket.ticket_number,
            title="Laptop power failure",
            category=TicketCategory.HARDWARE,
            requester_email="updated@example.com",
        )

        self.assertEqual(
            updated.title,
            "Laptop power failure",
        )

        self.assertEqual(
            updated.requester_email,
            "updated@example.com",
        )

    def test_resolve_requires_resolution(self) -> None:
        ticket = self.create_ticket()

        with self.assertRaises(
            InvalidStatusTransitionError
        ):
            self.service.change_status(
                ticket.ticket_number,
                TicketStatus.RESOLVED,
            )

    def test_complete_status_workflow(self) -> None:
        ticket = self.create_ticket()

        self.service.change_status(
            ticket.ticket_number,
            TicketStatus.IN_PROGRESS,
        )

        self.service.add_resolution(
            ticket.ticket_number,
            "Power adapter was replaced.",
        )

        resolved = self.service.change_status(
            ticket.ticket_number,
            TicketStatus.RESOLVED,
        )

        self.assertEqual(
            resolved.status,
            TicketStatus.RESOLVED,
        )

        self.assertIsNotNone(
            resolved.resolved_at
        )

        closed = self.service.close_ticket(
            ticket.ticket_number
        )

        self.assertEqual(
            closed.status,
            TicketStatus.CLOSED,
        )

        self.assertIsNotNone(
            closed.closed_at
        )

    def test_invalid_status_transition_is_blocked(self) -> None:
        ticket = self.create_ticket()

        with self.assertRaises(
            InvalidStatusTransitionError
        ):
            self.service.change_status(
                ticket.ticket_number,
                TicketStatus.CLOSED,
            )

    def test_closed_ticket_cannot_be_edited(self) -> None:
        ticket = self.create_ticket()

        self.service.add_resolution(
            ticket.ticket_number,
            "Hardware issue resolved.",
        )

        self.service.change_status(
            ticket.ticket_number,
            TicketStatus.RESOLVED,
        )

        self.service.close_ticket(
            ticket.ticket_number
        )

        with self.assertRaises(
            ValidationError
        ):
            self.service.update_ticket_details(
                ticket.ticket_number,
                title="Changed after closing",
            )

    def test_empty_search_is_rejected(self) -> None:
        with self.assertRaises(
            ValidationError
        ):
            self.service.search_tickets(
                "   "
            )

    def test_full_audit_history(self) -> None:
        ticket = self.create_ticket()

        self.service.assign_ticket(
            ticket.ticket_number,
            "Support Engineer",
        )

        self.service.change_priority(
            ticket.ticket_number,
            TicketPriority.CRITICAL,
        )

        self.service.add_resolution(
            ticket.ticket_number,
            "Faulty adapter replaced.",
        )

        self.service.change_status(
            ticket.ticket_number,
            TicketStatus.IN_PROGRESS,
        )

        self.service.change_status(
            ticket.ticket_number,
            TicketStatus.RESOLVED,
        )

        self.service.close_ticket(
            ticket.ticket_number
        )

        history = self.service.get_ticket_history(
            ticket.ticket_number
        )

        actions = [
            item["action"]
            for item in history
        ]

        self.assertEqual(
            actions,
            [
                "CREATED",
                "ASSIGNED",
                "PRIORITY_CHANGED",
                "RESOLUTION_UPDATED",
                "STATUS_CHANGED",
                "STATUS_CHANGED",
                "STATUS_CHANGED",
            ],
        )


if __name__ == "__main__":
    unittest.main()
