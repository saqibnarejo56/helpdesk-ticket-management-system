import json
from pathlib import Path


class AlertReportGenerator:
    """Generate an alert report from ticket analysis results."""

    def __init__(self, output_directory: Path | str) -> None:
        self.output_directory = Path(output_directory)

    def generate(
        self,
        analysis: dict,
        filename: str = "helpdesk_alerts.json",
    ) -> Path:
        """Create a JSON report containing tickets requiring attention."""

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        attention_required = analysis.get(
            "attention_required",
            [],
        )

        unassigned_tickets = analysis.get(
            "unassigned_tickets",
            [],
        )

        active_tickets = analysis.get(
            "active_tickets",
            [],
        )

        alert_report = {
            "attention_required_count": len(
                attention_required
            ),
            "attention_required": attention_required,
            "unassigned_count": len(
                unassigned_tickets
            ),
            "unassigned_tickets": unassigned_tickets,
            "active_count": len(
                active_tickets
            ),
            "active_tickets": active_tickets,
        }

        output_path = self.output_directory / filename

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                alert_report,
                file,
                indent=2,
            )

        return output_path