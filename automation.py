from pathlib import Path

from src.automation.alert_report import AlertReportGenerator
from src.automation.report_generator import ReportGenerator
from src.automation.ticket_analyzer import TicketAnalyzer
from src.database.connection import DatabaseConnection
from src.repositories.ticket_repository import TicketRepository


def main() -> None:
    project_root = Path(__file__).resolve().parent
    database_path = project_root / "data" / "helpdesk.db"
    reports_directory = project_root / "reports"

    database = DatabaseConnection(database_path)
    repository = TicketRepository(database)
    analyzer = TicketAnalyzer(repository)

    analysis = analyzer.analyze()

    report_generator = ReportGenerator(
        reports_directory
    )

    alert_generator = AlertReportGenerator(
        reports_directory
    )

    json_path = report_generator.generate_json_report(
        analysis
    )

    csv_path = report_generator.generate_active_tickets_report(
        analysis
    )

    alert_path = alert_generator.generate(
        analysis
    )

    print()
    print("=" * 50)
    print("HELPDESK AUTOMATION REPORT")
    print("=" * 50)
    print(f"Total Tickets       : {analysis['total_tickets']}")
    print(
        f"Active Tickets      : "
        f"{len(analysis['active_tickets'])}"
    )
    print(
        f"Attention Required  : "
        f"{len(analysis['attention_required'])}"
    )
    print(
        f"Unassigned Tickets  : "
        f"{len(analysis['unassigned_tickets'])}"
    )
    print("-" * 50)
    print(f"JSON Report         : {json_path}")
    print(f"CSV Report          : {csv_path}")
    print(f"Alert Report        : {alert_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()