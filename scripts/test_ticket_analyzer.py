from pathlib import Path

from src.automation.ticket_analyzer import TicketAnalyzer
from src.database.connection import DatabaseConnection
from src.repositories.ticket_repository import TicketRepository


def main() -> None:
    database_path = Path("data/helpdesk.db")

    database = DatabaseConnection(database_path)
    repository = TicketRepository(database)
    analyzer = TicketAnalyzer(repository)

    result = analyzer.analyze()

    print()
    print("AUTOMATION ANALYSIS RESULT")
    print("-" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()