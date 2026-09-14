import sqlite3
from datetime import datetime, timezone

from src.database.connection import DatabaseConnection
from src.exceptions.exceptions import DatabaseError


class TicketHistoryRepository:
    """Stores and retrieves the audit history of helpdesk tickets."""

    def __init__(
        self,
        database: DatabaseConnection,
    ) -> None:
        self.database = database

    def record(
        self,
        ticket_id: int,
        action: str,
        field_name: str | None = None,
        old_value: str | None = None,
        new_value: str | None = None,
    ) -> None:
        """Record a single ticket audit event."""

        if ticket_id <= 0:
            raise DatabaseError(
                "Ticket ID must be a positive integer."
            )

        action = action.strip()

        if not action:
            raise DatabaseError(
                "History action cannot be empty."
            )

        connection: sqlite3.Connection | None = None

        try:
            connection = self.database.connect()

            connection.execute(
                """
                INSERT INTO ticket_history (
                    ticket_id,
                    action,
                    field_name,
                    old_value,
                    new_value,
                    changed_at
                )
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    ticket_id,
                    action,
                    field_name,
                    old_value,
                    new_value,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )

            connection.commit()

        except sqlite3.IntegrityError as exc:
            if connection is not None:
                connection.rollback()

            raise DatabaseError(
                f"Unable to record ticket history: {exc}"
            ) from exc

        except sqlite3.Error as exc:
            if connection is not None:
                connection.rollback()

            raise DatabaseError(
                f"Database error while recording "
                f"ticket history: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()

    def get_by_ticket_id(
        self,
        ticket_id: int,
    ) -> list[dict[str, object]]:
        """Return the audit history for one ticket."""

        connection: sqlite3.Connection | None = None

        try:
            connection = self.database.connect()

            rows = connection.execute(
                """
                SELECT
                    id,
                    ticket_id,
                    action,
                    field_name,
                    old_value,
                    new_value,
                    changed_at
                FROM ticket_history
                WHERE ticket_id = ?
                ORDER BY id ASC;
                """,
                (ticket_id,),
            ).fetchall()

            return [
                {
                    "id": row["id"],
                    "ticket_id": row["ticket_id"],
                    "action": row["action"],
                    "field_name": row["field_name"],
                    "old_value": row["old_value"],
                    "new_value": row["new_value"],
                    "changed_at": row["changed_at"],
                }
                for row in rows
            ]

        except sqlite3.Error as exc:
            raise DatabaseError(
                f"Unable to retrieve ticket history: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()
