import unittest
from typing import cast

from src.exceptions.exceptions import ValidationError
from src.models.ticket import (
    Ticket,
    TicketCategory,
    TicketPriority,
)
from src.validators.ticket_validator import TicketValidator


class TicketValidatorTests(unittest.TestCase):

    @staticmethod
    def create_valid_ticket() -> Ticket:
        return Ticket(
            ticket_number="HD-00001",
            title="Laptop not starting",
            description=(
                "Laptop does not power on after "
                "pressing the power button."
            ),
            category=TicketCategory.HARDWARE,
            requester_name="Test User",
            requester_email="test@example.com",
        )

    def test_valid_ticket_passes_validation(self) -> None:
        ticket = self.create_valid_ticket()

        TicketValidator.validate_ticket(
            ticket
        )

    def test_invalid_email_is_rejected(self) -> None:
        ticket = self.create_valid_ticket()
        ticket.requester_email = "invalid-email"

        with self.assertRaises(ValidationError):
            TicketValidator.validate_ticket(
                ticket
            )

    def test_short_title_is_rejected(self) -> None:
        ticket = self.create_valid_ticket()
        ticket.title = "A"

        with self.assertRaises(ValidationError):
            TicketValidator.validate_ticket(
                ticket
            )

    def test_invalid_ticket_number_is_rejected(self) -> None:
        ticket = self.create_valid_ticket()
        ticket.ticket_number = "TICKET-1"

        with self.assertRaises(ValidationError):
            TicketValidator.validate_ticket(
                ticket
            )

    def test_short_description_is_rejected(self) -> None:
        ticket = self.create_valid_ticket()
        ticket.description = "Bad"

        with self.assertRaises(ValidationError):
            TicketValidator.validate_ticket(
                ticket
            )

    def test_empty_requester_name_is_rejected(self) -> None:
        ticket = self.create_valid_ticket()
        ticket.requester_name = " "

        with self.assertRaises(ValidationError):
            TicketValidator.validate_ticket(
                ticket
            )

    def test_invalid_category_is_rejected(self) -> None:
        ticket = self.create_valid_ticket()

        ticket.category = cast(
            TicketCategory,
            "Invalid Category",
        )

        with self.assertRaises(ValidationError):
            TicketValidator.validate_ticket(
                ticket
            )

    def test_invalid_priority_is_rejected(self) -> None:
        ticket = self.create_valid_ticket()

        ticket.priority = cast(
            TicketPriority,
            "URGENT",
        )

        with self.assertRaises(ValidationError):
            TicketValidator.validate_ticket(
                ticket
            )

    def test_blank_assigned_to_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            TicketValidator.validate_assigned_to(
                "   "
            )

    def test_blank_resolution_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            TicketValidator.validate_resolution(
                "   "
            )


if __name__ == "__main__":
    unittest.main()
