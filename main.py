from src.application import HelpdeskApplication
from src.cli.menu import HelpdeskMenu
from src.exceptions.exceptions import HelpdeskError


def main() -> int:
    """Start the Helpdesk Ticket Management System."""

    application = HelpdeskApplication()

    try:
        application.initialize()

        ticket_service = application.get_ticket_service()

        menu = HelpdeskMenu(
            ticket_service
        )

        menu.run()

        return 0

    except HelpdeskError as exc:
        if application.logger is not None:
            application.logger.exception(
                "Application terminated because of "
                "a helpdesk error."
            )

        print(
            f"\nApplication error: {exc}"
        )

        return 1

    except KeyboardInterrupt:
        if application.logger is not None:
            application.logger.info(
                "Application interrupted by the user."
            )

        print(
            "\nApplication interrupted by user."
        )

        return 130

    except Exception:
        if application.logger is not None:
            application.logger.exception(
                "Unexpected fatal application error."
            )

        print(
            "\nAn unexpected error occurred."
        )
        print(
            "Check logs/helpdesk.log for details."
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
