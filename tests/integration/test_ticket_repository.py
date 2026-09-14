import tempfile
import unittest
from pathlib import Path

from src.database.connection import DatabaseConnection
from src.database.schema import DatabaseSchema
from src.exceptions.exceptions import TicketNotFoundError
from src.models.ticket import (
    Ticket,
    TicketCategory,
    TicketPriority,
)
from src.repositories.ticket_repository import TicketRepository


class TicketRepositoryTests(unittest.TestCase):

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

        self.repository = TicketRepository(
            database
        )

    def tearDown(self) -> None:
        self.database_path.unlink(
            missing_ok=True
        )

    def create_ticket(
        self,
        ticket_number: str = "HD-00001",
        title: str = "Laptop not starting",
    ) -> Ticket:
        return Ticket(
            ticket_number=ticket_number,
            title=title,
            description=(
                "Laptop does not power on after "
                "pressing the power button."
            ),
            category=TicketCategory.HARDWARE,
            requester_name="Test User",
            requester_email="test@example.com",
        )

    def test_create_and_retrieve_ticket(self) -> None:
        ticket = self.create_ticket()

        saved = self.repository.create(
            ticket
        )

        self.assertIsNotNone(
            saved.id
        )

        loaded = self.repository.get_by_ticket_number(
            "HD-00001"
        )

        self.assertEqual(
            loaded.title,
            "Laptop not starting",
        )

        self.assertEqual(
            loaded.ticket_number,
            "HD-00001",
        )

    def test_list_all_tickets(self) -> None:
        self.repository.create(
            self.create_ticket(
                "HD-00001",
                "Laptop issue",
            )
        )

        self.repository.create(
            self.create_ticket(
                "HD-00002",
                "Keyboard issue",
            )
        )

        tickets = self.repository.list_all()

        self.assertEqual(
            len(tickets),
            2,
        )

    def test_search_ticket(self) -> None:
        self.repository.create(
            self.create_ticket(
                "HD-00001",
                "Laptop not starting",
            )
        )

        results = self.repository.search(
            "Laptop"
        )

        self.assertEqual(
            len(results),
            1,
        )

        self.assertEqual(
            results[0].ticket_number,
            "HD-00001",
        )

    def test_update_ticket(self) -> None:
        ticket = self.repository.create(
            self.create_ticket()
        )

        ticket.priority = TicketPriority.HIGH
        ticket.title = "Laptop power failure"
        ticket.touch()

        self.repository.update(
            ticket
        )

        ticket_id = ticket.id

        if ticket_id is None:
            self.fail(
                "Created ticket did not receive a database ID."
            )

        updated = self.repository.get_by_id(
            ticket_id
        )

        self.assertEqual(
            updated.priority,
            TicketPriority.HIGH,
        )

        self.assertEqual(
            updated.title,
            "Laptop power failure",
        )

    def test_next_ticket_number(self) -> None:
        first_number = (
            self.repository.get_next_ticket_number()
        )

        self.assertEqual(
            first_number,
            "HD-00001",
        )

        self.repository.create(
            self.create_ticket(
                first_number
            )
        )

        second_number = (
            self.repository.get_next_ticket_number()
        )

        self.assertEqual(
            second_number,
            "HD-00002",
        )

    def test_missing_ticket_raises_error(self) -> None:
        with self.assertRaises(
            TicketNotFoundError
        ):
            self.repository.get_by_ticket_number(
                "HD-99999"
            )


if __name__ == "__main__":
    unittest.main()
