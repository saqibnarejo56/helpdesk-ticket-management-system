import json
from pathlib import Path
from tempfile import TemporaryDirectory

from src.automation.report_generator import ReportGenerator
from src.automation.ticket_analyzer import TicketAnalyzer
from src.database.connection import DatabaseConnection
from src.repositories.ticket_repository import TicketRepository


def main() -> None:
    database_path = Path("data/helpdesk.db")

    database = DatabaseConnection(database_path)
    repository = TicketRepository(database)
    analyzer = TicketAnalyzer(repository)

    analysis = analyzer.analyze()

    with TemporaryDirectory() as temporary_directory:
        generator = ReportGenerator(temporary_directory)

        json_path = generator.generate_json_report(
            analysis
        )

        csv_path = generator.generate_active_tickets_report(
            analysis
        )

        print()
        print("REPORT GENERATION RESULT")
        print("-" * 40)

        print(f"JSON report: {json_path}")
        print(f"CSV report : {csv_path}")

        print()
        print("JSON CONTENT")
        print("-" * 40)

        with json_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            generated_analysis = json.load(file)

        print(json.dumps(
            generated_analysis,
            indent=2,
        ))

        print()
        print("CSV CONTENT")
        print("-" * 40)

        print(csv_path.read_text(
            encoding="utf-8"
        ))


if __name__ == "__main__":
    main()