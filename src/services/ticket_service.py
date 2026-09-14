from datetime import datetime, timezone

from src.exceptions.exceptions import (
    DatabaseError,
    InvalidStatusTransitionError,
    ValidationError,
)
from src.models.ticket import (
    Ticket,
    TicketCategory,
    TicketPriority,
    TicketStatus,
)
from src.repositories.ticket_history_repository import (
    TicketHistoryRepository,
)
from src.repositories.ticket_repository import TicketRepository
from src.validators.ticket_validator import TicketValidator


class TicketService:
    """Implements the business rules of the helpdesk system."""

    ALLOWED_STATUS_TRANSITIONS = {
        TicketStatus.OPEN: {
            TicketStatus.IN_PROGRESS,
            TicketStatus.RESOLVED,
        },
        TicketStatus.IN_PROGRESS: {
            TicketStatus.RESOLVED,
        },
        TicketStatus.RESOLVED: {
            TicketStatus.CLOSED,
        },
        TicketStatus.CLOSED: set(),
    }

    def __init__(
        self,
        ticket_repository: TicketRepository,
        history_repository: TicketHistoryRepository,
    ) -> None:
        self.ticket_repository = ticket_repository
        self.history_repository = history_repository

    def create_ticket(
        self,
        title: str,
        description: str,
        category: TicketCategory,
        requester_name: str,
        requester_email: str,
        priority: TicketPriority = TicketPriority.MEDIUM,
    ) -> Ticket:
        """Create, validate, persist, and audit a new ticket."""

        ticket_number = (
            self.ticket_repository.get_next_ticket_number()
        )

        ticket = Ticket(
            ticket_number=ticket_number,
            title=title.strip(),
            description=description.strip(),
            category=category,
            requester_name=requester_name.strip(),
            requester_email=requester_email.strip(),
            priority=priority,
        )

        TicketValidator.validate_ticket(ticket)

        saved_ticket = self.ticket_repository.create(
            ticket
        )

        if saved_ticket.id is None:
            raise DatabaseError(
                "Created ticket did not receive a database ID."
            )

        self.history_repository.record(
            ticket_id=saved_ticket.id,
            action="CREATED",
            field_name="status",
            old_value=None,
            new_value=saved_ticket.status.value,
        )

        return saved_ticket

    def get_ticket(
        self,
        ticket_number: str,
    ) -> Ticket:
        """Retrieve one ticket by its public ticket number."""

        return self.ticket_repository.get_by_ticket_number(
            ticket_number.strip()
        )

    def list_tickets(self) -> list[Ticket]:
        """Return all helpdesk tickets."""

        return self.ticket_repository.list_all()

    def search_tickets(
        self,
        keyword: str,
    ) -> list[Ticket]:
        """Search tickets by keyword."""

        keyword = keyword.strip()

        if not keyword:
            raise ValidationError(
                "Search keyword cannot be empty."
            )

        return self.ticket_repository.search(
            keyword
        )

    def update_ticket_details(
        self,
        ticket_number: str,
        *,
        title: str | None = None,
        description: str | None = None,
        category: TicketCategory | None = None,
        requester_name: str | None = None,
        requester_email: str | None = None,
    ) -> Ticket:
        """Update editable ticket details."""

        ticket = self.get_ticket(
            ticket_number
        )

        if ticket.status == TicketStatus.CLOSED:
            raise ValidationError(
                "Closed tickets cannot be edited."
            )

        changes: list[
            tuple[str, str | None, str | None]
        ] = []

        if title is not None:
            old_value = ticket.title
            ticket.title = title.strip()

            changes.append(
                (
                    "title",
                    old_value,
                    ticket.title,
                )
            )

        if description is not None:
            old_value = ticket.description
            ticket.description = description.strip()

            changes.append(
                (
                    "description",
                    old_value,
                    ticket.description,
                )
            )

        if category is not None:
            old_value = ticket.category.value
            ticket.category = category

            changes.append(
                (
                    "category",
                    old_value,
                    ticket.category.value,
                )
            )

        if requester_name is not None:
            old_value = ticket.requester_name
            ticket.requester_name = requester_name.strip()

            changes.append(
                (
                    "requester_name",
                    old_value,
                    ticket.requester_name,
                )
            )

        if requester_email is not None:
            old_value = ticket.requester_email
            ticket.requester_email = requester_email.strip()

            changes.append(
                (
                    "requester_email",
                    old_value,
                    ticket.requester_email,
                )
            )

        if not changes:
            raise ValidationError(
                "No ticket changes were provided."
            )

        TicketValidator.validate_ticket(
            ticket
        )

        ticket.touch()

        updated_ticket = self.ticket_repository.update(
            ticket
        )

        if updated_ticket.id is None:
            raise DatabaseError(
                "Updated ticket has no database ID."
            )

        for field_name, old_value, new_value in changes:
            if old_value == new_value:
                continue

            self.history_repository.record(
                ticket_id=updated_ticket.id,
                action="UPDATED",
                field_name=field_name,
                old_value=old_value,
                new_value=new_value,
            )

        return updated_ticket

    def assign_ticket(
        self,
        ticket_number: str,
        assigned_to: str,
    ) -> Ticket:
        """Assign a ticket to a support technician."""

        ticket = self.get_ticket(
            ticket_number
        )

        if ticket.status == TicketStatus.CLOSED:
            raise ValidationError(
                "A closed ticket cannot be assigned."
            )

        assigned_to = assigned_to.strip()

        TicketValidator.validate_assigned_to(
            assigned_to
        )

        old_value = ticket.assigned_to

        if old_value == assigned_to:
            raise ValidationError(
                "Ticket is already assigned to this technician."
            )

        ticket.assigned_to = assigned_to
        ticket.touch()

        updated_ticket = self.ticket_repository.update(
            ticket
        )

        if updated_ticket.id is None:
            raise DatabaseError(
                "Updated ticket has no database ID."
            )

        self.history_repository.record(
            ticket_id=updated_ticket.id,
            action="ASSIGNED",
            field_name="assigned_to",
            old_value=old_value,
            new_value=assigned_to,
        )

        return updated_ticket

    def change_priority(
        self,
        ticket_number: str,
        priority: TicketPriority,
    ) -> Ticket:
        """Change the priority of an active ticket."""

        ticket = self.get_ticket(
            ticket_number
        )

        if ticket.status == TicketStatus.CLOSED:
            raise ValidationError(
                "Priority of a closed ticket cannot be changed."
            )

        TicketValidator.validate_priority(
            priority
        )

        old_priority = ticket.priority

        if old_priority == priority:
            raise ValidationError(
                "Ticket already has this priority."
            )

        ticket.priority = priority
        ticket.touch()

        updated_ticket = self.ticket_repository.update(
            ticket
        )

        if updated_ticket.id is None:
            raise DatabaseError(
                "Updated ticket has no database ID."
            )

        self.history_repository.record(
            ticket_id=updated_ticket.id,
            action="PRIORITY_CHANGED",
            field_name="priority",
            old_value=old_priority.value,
            new_value=priority.value,
        )

        return updated_ticket

    def add_resolution(
        self,
        ticket_number: str,
        resolution: str,
    ) -> Ticket:
        """Add or update the resolution of an active ticket."""

        ticket = self.get_ticket(
            ticket_number
        )

        if ticket.status == TicketStatus.CLOSED:
            raise ValidationError(
                "Resolution of a closed ticket cannot be changed."
            )

        resolution = resolution.strip()

        TicketValidator.validate_resolution(
            resolution
        )

        old_resolution = ticket.resolution

        if old_resolution == resolution:
            raise ValidationError(
                "The same resolution is already recorded."
            )

        ticket.resolution = resolution
        ticket.touch()

        updated_ticket = self.ticket_repository.update(
            ticket
        )

        if updated_ticket.id is None:
            raise DatabaseError(
                "Updated ticket has no database ID."
            )

        self.history_repository.record(
            ticket_id=updated_ticket.id,
            action="RESOLUTION_UPDATED",
            field_name="resolution",
            old_value=old_resolution,
            new_value=resolution,
        )

        return updated_ticket

    def change_status(
        self,
        ticket_number: str,
        new_status: TicketStatus,
    ) -> Ticket:
        """Change ticket status according to workflow rules."""

        TicketValidator.validate_status(
            new_status
        )

        ticket = self.get_ticket(
            ticket_number
        )

        old_status = ticket.status

        if old_status == new_status:
            raise InvalidStatusTransitionError(
                f"Ticket is already {new_status.value}."
            )

        allowed_statuses = (
            self.ALLOWED_STATUS_TRANSITIONS[
                old_status
            ]
        )

        if new_status not in allowed_statuses:
            raise InvalidStatusTransitionError(
                f"Status cannot change from "
                f"{old_status.value} to "
                f"{new_status.value}."
            )

        if (
            new_status == TicketStatus.RESOLVED
            and not ticket.resolution
        ):
            raise InvalidStatusTransitionError(
                "A resolution must be added before "
                "the ticket can be resolved."
            )

        current_time = datetime.now(
            timezone.utc
        )

        ticket.status = new_status

        if new_status == TicketStatus.RESOLVED:
            ticket.resolved_at = current_time

        if new_status == TicketStatus.CLOSED:
            if not ticket.resolution:
                raise InvalidStatusTransitionError(
                    "A resolved ticket must have "
                    "a resolution before closing."
                )

            ticket.closed_at = current_time

        ticket.touch()

        updated_ticket = self.ticket_repository.update(
            ticket
        )

        if updated_ticket.id is None:
            raise DatabaseError(
                "Updated ticket has no database ID."
            )

        self.history_repository.record(
            ticket_id=updated_ticket.id,
            action="STATUS_CHANGED",
            field_name="status",
            old_value=old_status.value,
            new_value=new_status.value,
        )

        return updated_ticket

    def close_ticket(
        self,
        ticket_number: str,
    ) -> Ticket:
        """Close a ticket that has already been resolved."""

        return self.change_status(
            ticket_number,
            TicketStatus.CLOSED,
        )

    def get_ticket_history(
        self,
        ticket_number: str,
    ) -> list[dict[str, object]]:
        """Return the complete audit history of a ticket."""

        ticket = self.get_ticket(
            ticket_number
        )

        if ticket.id is None:
            raise DatabaseError(
                "Ticket has no database ID."
            )

        return self.history_repository.get_by_ticket_id(
            ticket.id
        )
