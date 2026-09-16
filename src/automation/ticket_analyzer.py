from collections import Counter

from src.repositories.ticket_repository import TicketRepository


class TicketAnalyzer:
    """
    Analyzes helpdesk tickets and produces automation metrics.
    """

    def __init__(
        self,
        ticket_repository: TicketRepository,
    ) -> None:
        self.ticket_repository = ticket_repository

    def analyze(self) -> dict:
        """
        Generate ticket analysis summary.
        """

        tickets = self.ticket_repository.list_all()

        status_summary = Counter(
            ticket.status.value
            for ticket in tickets
        )

        priority_summary = Counter(
            ticket.priority.value
            for ticket in tickets
        )

        active_tickets = [
            ticket.ticket_number
            for ticket in tickets
            if ticket.status.value in {
                "OPEN",
                "IN_PROGRESS",
            }
        ]

        attention_required = [
            ticket.ticket_number
            for ticket in tickets
            if (
                ticket.priority.value in {
                    "HIGH",
                    "CRITICAL",
                }
                and ticket.status.value != "CLOSED"
            )
        ]

        unassigned_tickets = [
            ticket.ticket_number
            for ticket in tickets
            if not ticket.assigned_to
        ]

        return {
            "total_tickets": len(tickets),
            "status_summary": dict(status_summary),
            "priority_summary": dict(priority_summary),
            "active_tickets": active_tickets,
            "attention_required": attention_required,
            "unassigned_tickets": unassigned_tickets,
        }
