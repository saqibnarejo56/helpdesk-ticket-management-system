from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class TicketCategory(str, Enum):
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    NETWORK = "Network"
    EMAIL = "Email"
    ACCESS = "Access"
    PRINTER = "Printer"
    OTHER = "Other"


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


@dataclass(slots=True)
class Ticket:
    ticket_number: str
    title: str
    description: str
    category: TicketCategory
    requester_name: str
    requester_email: str

    priority: TicketPriority = TicketPriority.MEDIUM
    status: TicketStatus = TicketStatus.OPEN

    assigned_to: str | None = None
    resolution: str | None = None

    id: int | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    resolved_at: datetime | None = None
    closed_at: datetime | None = None

    def touch(self) -> None:
        """Update the ticket's last-modified timestamp."""
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, object]:
        """Return a serializable representation of the ticket."""

        return {
            "id": self.id,
            "ticket_number": self.ticket_number,
            "title": self.title,
            "description": self.description,
            "category": self.category.value,
            "priority": self.priority.value,
            "status": self.status.value,
            "requester_name": self.requester_name,
            "requester_email": self.requester_email,
            "assigned_to": self.assigned_to,
            "resolution": self.resolution,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "resolved_at": (
                self.resolved_at.isoformat()
                if self.resolved_at
                else None
            ),
            "closed_at": (
                self.closed_at.isoformat()
                if self.closed_at
                else None
            ),
        }
