import csv
import json
from pathlib import Path


class ReportGenerator:
    """Generate JSON and CSV reports from ticket analysis results."""

    def __init__(self, output_directory: Path | str) -> None:
        self.output_directory = Path(output_directory)

    def generate_json_report(
        self,
        analysis: dict,
        filename: str = "helpdesk_summary.json",
    ) -> Path:
        """Write the complete analysis result as JSON."""

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = self.output_directory / filename

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                analysis,
                file,
                indent=2,
            )

        return output_path

    def generate_active_tickets_report(
        self,
        analysis: dict,
        filename: str = "active_tickets.csv",
    ) -> Path:
        """Write active ticket numbers as a CSV report."""

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = self.output_directory / filename

        active_tickets = analysis.get(
            "active_tickets",
            [],
        )

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            writer.writerow(["ticket_number"])

            for ticket_number in active_tickets:
                writer.writerow([ticket_number])

        return output_path