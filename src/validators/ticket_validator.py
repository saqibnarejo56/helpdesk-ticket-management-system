import re

from src.exceptions.exceptions import ValidationError
from src.models.ticket import (
    Ticket,
    TicketCategory,
    TicketPriority,
    TicketStatus,
)


class TicketValidator:
    """Validates ticket data before it reaches the database."""

    EMAIL_PATTERN = re.compile(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    TICKET_NUMBER_PATTERN = re.compile(
        r"^HD-\d{5,}$"
    )

    @classmethod
    def validate_ticket(cls, ticket: Ticket) -> None:
        """Validate all core fields of a ticket."""

        cls.validate_ticket_number(
            ticket.ticket_number
        )

        cls.validate_title(
            ticket.title
        )

        cls.validate_description(
            ticket.description
        )

        cls.validate_requester_name(
            ticket.requester_name
        )

        cls.validate_email(
            ticket.requester_email
        )

        cls.validate_category(
            ticket.category
        )

        cls.validate_priority(
            ticket.priority
        )

        cls.validate_status(
            ticket.status
        )

        cls.validate_assigned_to(
            ticket.assigned_to
        )

        cls.validate_resolution(
            ticket.resolution
        )

    @classmethod
    def validate_ticket_number(
        cls,
        ticket_number: str,
    ) -> None:
        if not isinstance(ticket_number, str):
            raise ValidationError(
                "Ticket number must be a string."
            )

        ticket_number = ticket_number.strip()

        if not cls.TICKET_NUMBER_PATTERN.fullmatch(
            ticket_number
        ):
            raise ValidationError(
                "Ticket number must use the format "
                "'HD-00001'."
            )

    @staticmethod
    def validate_title(title: str) -> None:
        if not isinstance(title, str):
            raise ValidationError(
                "Ticket title must be a string."
            )

        title = title.strip()

        if len(title) < 3:
            raise ValidationError(
                "Ticket title must contain at least "
                "3 characters."
            )

        if len(title) > 120:
            raise ValidationError(
                "Ticket title cannot exceed "
                "120 characters."
            )

    @staticmethod
    def validate_description(
        description: str,
    ) -> None:
        if not isinstance(description, str):
            raise ValidationError(
                "Ticket description must be a string."
            )

        description = description.strip()

        if len(description) < 5:
            raise ValidationError(
                "Ticket description must contain at least "
                "5 characters."
            )

        if len(description) > 2000:
            raise ValidationError(
                "Ticket description cannot exceed "
                "2000 characters."
            )

    @staticmethod
    def validate_requester_name(
        requester_name: str,
    ) -> None:
        if not isinstance(requester_name, str):
            raise ValidationError(
                "Requester name must be a string."
            )

        requester_name = requester_name.strip()

        if len(requester_name) < 2:
            raise ValidationError(
                "Requester name must contain at least "
                "2 characters."
            )

        if len(requester_name) > 100:
            raise ValidationError(
                "Requester name cannot exceed "
                "100 characters."
            )

    @classmethod
    def validate_email(
        cls,
        email: str,
    ) -> None:
        if not isinstance(email, str):
            raise ValidationError(
                "Requester email must be a string."
            )

        email = email.strip()

        if len(email) > 254:
            raise ValidationError(
                "Requester email is too long."
            )

        if not cls.EMAIL_PATTERN.fullmatch(email):
            raise ValidationError(
                "Requester email address is invalid."
            )

    @staticmethod
    def validate_category(
        category: TicketCategory,
    ) -> None:
        if not isinstance(
            category,
            TicketCategory,
        ):
            raise ValidationError(
                "Invalid ticket category."
            )

    @staticmethod
    def validate_priority(
        priority: TicketPriority,
    ) -> None:
        if not isinstance(
            priority,
            TicketPriority,
        ):
            raise ValidationError(
                "Invalid ticket priority."
            )

    @staticmethod
    def validate_status(
        status: TicketStatus,
    ) -> None:
        if not isinstance(
            status,
            TicketStatus,
        ):
            raise ValidationError(
                "Invalid ticket status."
            )

    @staticmethod
    def validate_assigned_to(
        assigned_to: str | None,
    ) -> None:
        if assigned_to is None:
            return

        if not isinstance(assigned_to, str):
            raise ValidationError(
                "Assigned technician name must be a string."
            )

        assigned_to = assigned_to.strip()

        if not assigned_to:
            raise ValidationError(
                "Assigned technician name cannot be empty."
            )

        if len(assigned_to) > 100:
            raise ValidationError(
                "Assigned technician name cannot exceed "
                "100 characters."
            )

    @staticmethod
    def validate_resolution(
        resolution: str | None,
    ) -> None:
        if resolution is None:
            return

        if not isinstance(resolution, str):
            raise ValidationError(
                "Resolution must be a string."
            )

        resolution = resolution.strip()

        if not resolution:
            raise ValidationError(
                "Resolution cannot be empty."
            )

        if len(resolution) > 2000:
            raise ValidationError(
                "Resolution cannot exceed "
                "2000 characters."
            )
