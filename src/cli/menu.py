import logging

from src.exceptions.exceptions import HelpdeskError
from src.models.ticket import (
    Ticket,
    TicketCategory,
    TicketPriority,
    TicketStatus,
)
from src.services.ticket_service import TicketService


class HelpdeskMenu:
    """Interactive command-line interface for the helpdesk system."""

    def __init__(
        self,
        ticket_service: TicketService,
    ) -> None:
        self.ticket_service = ticket_service
        self.logger = logging.getLogger("helpdesk")

    def run(self) -> None:
        """Run the main application menu."""

        self.logger.info(
            "Interactive helpdesk menu started."
        )

        while True:
            self._show_main_menu()

            choice = input(
                "Select an option: "
            ).strip()

            try:
                if choice == "1":
                    self._create_ticket()

                elif choice == "2":
                    self._view_ticket()

                elif choice == "3":
                    self._list_tickets()

                elif choice == "4":
                    self._search_tickets()

                elif choice == "5":
                    self._update_ticket()

                elif choice == "6":
                    self._assign_ticket()

                elif choice == "7":
                    self._change_priority()

                elif choice == "8":
                    self._change_status()

                elif choice == "9":
                    self._add_resolution()

                elif choice == "10":
                    self._view_history()

                elif choice == "0":
                    self.logger.info(
                        "User exited the application."
                    )

                    print(
                        "\nThank you for using the "
                        "Helpdesk Ticket Management System."
                    )
                    return

                else:
                    print(
                        "\nInvalid option. "
                        "Please select a valid menu number."
                    )

            except HelpdeskError as exc:
                self.logger.warning(
                    "Application operation failed: %s",
                    exc,
                )

                print(
                    f"\nError: {exc}"
                )

            except (ValueError, TypeError) as exc:
                self.logger.warning(
                    "Invalid user input: %s",
                    exc,
                )

                print(
                    f"\nInvalid input: {exc}"
                )

    @staticmethod
    def _show_main_menu() -> None:
        print(
            "\n"
            "============================================\n"
            "     HELPDESK TICKET MANAGEMENT SYSTEM\n"
            "============================================\n"
            "1.  Create Ticket\n"
            "2.  View Ticket\n"
            "3.  List All Tickets\n"
            "4.  Search Tickets\n"
            "5.  Update Ticket Details\n"
            "6.  Assign Ticket\n"
            "7.  Change Priority\n"
            "8.  Change Status\n"
            "9.  Add Resolution\n"
            "10. View Ticket History\n"
            "0.  Exit\n"
            "============================================"
        )

    def _create_ticket(self) -> None:
        print(
            "\n--- Create Ticket ---"
        )

        title = input(
            "Title: "
        ).strip()

        description = input(
            "Description: "
        ).strip()

        category = self._select_category()

        requester_name = input(
            "Requester name: "
        ).strip()

        requester_email = input(
            "Requester email: "
        ).strip()

        priority = self._select_priority(
            allow_default=True
        )

        ticket = self.ticket_service.create_ticket(
            title=title,
            description=description,
            category=category,
            requester_name=requester_name,
            requester_email=requester_email,
            priority=priority,
        )

        self.logger.info(
            "Ticket %s created through CLI.",
            ticket.ticket_number,
        )

        print(
            "\nTicket created successfully."
        )

        self._display_ticket(
            ticket
        )

    def _view_ticket(self) -> None:
        print(
            "\n--- View Ticket ---"
        )

        ticket_number = self._read_ticket_number()

        ticket = self.ticket_service.get_ticket(
            ticket_number
        )

        self._display_ticket(
            ticket
        )

    def _list_tickets(self) -> None:
        print(
            "\n--- All Tickets ---"
        )

        tickets = self.ticket_service.list_tickets()

        if not tickets:
            print(
                "No tickets found."
            )
            return

        for ticket in tickets:
            self._display_ticket_summary(
                ticket
            )

        print(
            f"\nTotal tickets: {len(tickets)}"
        )

    def _search_tickets(self) -> None:
        print(
            "\n--- Search Tickets ---"
        )

        keyword = input(
            "Search keyword: "
        )

        tickets = self.ticket_service.search_tickets(
            keyword
        )

        if not tickets:
            print(
                "No matching tickets found."
            )
            return

        for ticket in tickets:
            self._display_ticket_summary(
                ticket
            )

        print(
            f"\nMatches found: {len(tickets)}"
        )

    def _update_ticket(self) -> None:
        print(
            "\n--- Update Ticket Details ---"
        )

        ticket_number = self._read_ticket_number()

        current = self.ticket_service.get_ticket(
            ticket_number
        )

        print(
            "Press Enter to keep the existing value."
        )

        title = input(
            f"Title [{current.title}]: "
        ).strip()

        description = input(
            "Description "
            f"[{current.description}]: "
        ).strip()

        requester_name = input(
            "Requester name "
            f"[{current.requester_name}]: "
        ).strip()

        requester_email = input(
            "Requester email "
            f"[{current.requester_email}]: "
        ).strip()

        change_category = input(
            "Change category? (y/N): "
        ).strip().lower()

        category = None

        if change_category == "y":
            category = self._select_category()

        if (
            not title
            and not description
            and not requester_name
            and not requester_email
            and category is None
        ):
            print(
                "\nNo changes entered."
            )
            return

        updated = self.ticket_service.update_ticket_details(
            ticket_number,
            title=title or None,
            description=description or None,
            category=category,
            requester_name=requester_name or None,
            requester_email=requester_email or None,
        )

        self.logger.info(
            "Ticket %s details updated through CLI.",
            ticket_number,
        )

        print(
            "\nTicket updated successfully."
        )

        self._display_ticket(
            updated
        )

    def _assign_ticket(self) -> None:
        print(
            "\n--- Assign Ticket ---"
        )

        ticket_number = self._read_ticket_number()

        assigned_to = input(
            "Technician / support engineer name: "
        ).strip()

        ticket = self.ticket_service.assign_ticket(
            ticket_number,
            assigned_to,
        )

        self.logger.info(
            "Ticket %s assigned to %s.",
            ticket_number,
            ticket.assigned_to,
        )

        print(
            "\nTicket assigned successfully."
        )

        self._display_ticket(
            ticket
        )

    def _change_priority(self) -> None:
        print(
            "\n--- Change Priority ---"
        )

        ticket_number = self._read_ticket_number()

        priority = self._select_priority(
            allow_default=False
        )

        ticket = self.ticket_service.change_priority(
            ticket_number,
            priority,
        )

        self.logger.info(
            "Ticket %s priority changed to %s.",
            ticket_number,
            priority.value,
        )

        print(
            "\nPriority changed successfully."
        )

        self._display_ticket(
            ticket
        )

    def _change_status(self) -> None:
        print(
            "\n--- Change Status ---"
        )

        ticket_number = self._read_ticket_number()

        status = self._select_status()

        ticket = self.ticket_service.change_status(
            ticket_number,
            status,
        )

        self.logger.info(
            "Ticket %s status changed to %s.",
            ticket_number,
            status.value,
        )

        print(
            "\nStatus changed successfully."
        )

        self._display_ticket(
            ticket
        )

    def _add_resolution(self) -> None:
        print(
            "\n--- Add Resolution ---"
        )

        ticket_number = self._read_ticket_number()

        resolution = input(
            "Resolution: "
        ).strip()

        ticket = self.ticket_service.add_resolution(
            ticket_number,
            resolution,
        )

        self.logger.info(
            "Resolution recorded for ticket %s.",
            ticket_number,
        )

        print(
            "\nResolution saved successfully."
        )

        self._display_ticket(
            ticket
        )

    def _view_history(self) -> None:
        print(
            "\n--- Ticket History ---"
        )

        ticket_number = self._read_ticket_number()

        history = self.ticket_service.get_ticket_history(
            ticket_number
        )

        if not history:
            print(
                "No history found."
            )
            return

        print(
            f"\nHistory for {ticket_number}"
        )

        print(
            "-" * 72
        )

        for item in history:
            print(
                f"Action      : {item['action']}"
            )

            print(
                f"Field       : "
                f"{item['field_name'] or '-'}"
            )

            print(
                f"Old Value   : "
                f"{item['old_value'] or '-'}"
            )

            print(
                f"New Value   : "
                f"{item['new_value'] or '-'}"
            )

            print(
                f"Changed At  : {item['changed_at']}"
            )

            print(
                "-" * 72
            )

    @staticmethod
    def _read_ticket_number() -> str:
        return input(
            "Ticket number (example HD-00001): "
        ).strip().upper()

    @staticmethod
    def _select_category() -> TicketCategory:
        categories = list(
            TicketCategory
        )

        print(
            "\nCategories:"
        )

        for index, category in enumerate(
            categories,
            start=1,
        ):
            print(
                f"{index}. {category.value}"
            )

        choice = input(
            "Select category: "
        ).strip()

        try:
            index = int(choice) - 1
            return categories[index]

        except (
            ValueError,
            IndexError,
        ) as exc:
            raise ValueError(
                "Invalid category selection."
            ) from exc

    @staticmethod
    def _select_priority(
        allow_default: bool,
    ) -> TicketPriority:
        priorities = list(
            TicketPriority
        )

        print(
            "\nPriorities:"
        )

        for index, priority in enumerate(
            priorities,
            start=1,
        ):
            print(
                f"{index}. {priority.value}"
            )

        if allow_default:
            print(
                "Press Enter for MEDIUM."
            )

        choice = input(
            "Select priority: "
        ).strip()

        if allow_default and not choice:
            return TicketPriority.MEDIUM

        try:
            index = int(choice) - 1
            return priorities[index]

        except (
            ValueError,
            IndexError,
        ) as exc:
            raise ValueError(
                "Invalid priority selection."
            ) from exc

    @staticmethod
    def _select_status() -> TicketStatus:
        statuses = list(
            TicketStatus
        )

        print(
            "\nStatuses:"
        )

        for index, status in enumerate(
            statuses,
            start=1,
        ):
            print(
                f"{index}. {status.value}"
            )

        choice = input(
            "Select status: "
        ).strip()

        try:
            index = int(choice) - 1
            return statuses[index]

        except (
            ValueError,
            IndexError,
        ) as exc:
            raise ValueError(
                "Invalid status selection."
            ) from exc

    @staticmethod
    def _display_ticket(
        ticket: Ticket,
    ) -> None:
        print(
            "\n"
            "--------------------------------------------"
        )

        print(
            f"Ticket Number : {ticket.ticket_number}"
        )
        print(
            f"Title         : {ticket.title}"
        )
        print(
            f"Description   : {ticket.description}"
        )
        print(
            f"Category      : {ticket.category.value}"
        )
        print(
            f"Priority      : {ticket.priority.value}"
        )
        print(
            f"Status        : {ticket.status.value}"
        )
        print(
            f"Requester     : {ticket.requester_name}"
        )
        print(
            f"Email         : {ticket.requester_email}"
        )
        print(
            f"Assigned To   : {ticket.assigned_to or '-'}"
        )
        print(
            f"Resolution    : {ticket.resolution or '-'}"
        )
        print(
            f"Created At    : {ticket.created_at.isoformat()}"
        )
        print(
            f"Updated At    : {ticket.updated_at.isoformat()}"
        )
        print(
            "Resolved At   : "
            f"{ticket.resolved_at.isoformat() if ticket.resolved_at else '-'}"
        )
        print(
            "Closed At     : "
            f"{ticket.closed_at.isoformat() if ticket.closed_at else '-'}"
        )

        print(
            "--------------------------------------------"
        )

    @staticmethod
    def _display_ticket_summary(
        ticket: Ticket,
    ) -> None:
        print(
            f"{ticket.ticket_number:<10} | "
            f"{ticket.status.value:<11} | "
            f"{ticket.priority.value:<8} | "
            f"{ticket.category.value:<10} | "
            f"{ticket.title}"
        )
