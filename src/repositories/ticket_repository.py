import sqlite3
from datetime import datetime

from src.database.connection import DatabaseConnection
from src.exceptions.exceptions import (
    DatabaseError,
    TicketNotFoundError,
)
from src.models.ticket import (
    Ticket,
    TicketCategory,
    TicketPriority,
    TicketStatus,
)


class TicketRepository:
    """Handles ticket persistence and retrieval using SQLite."""

    def __init__(
        self,
        database: DatabaseConnection,
    ) -> None:
        self.database = database

    def create(self, ticket: Ticket) -> Ticket:
        """Insert a new ticket into the database."""

        connection: sqlite3.Connection | None = None

        try:
            connection = self.database.connect()

            cursor = connection.execute(
                """
                INSERT INTO tickets (
                    ticket_number,
                    title,
                    description,
                    category,
                    priority,
                    status,
                    requester_name,
                    requester_email,
                    assigned_to,
                    resolution,
                    created_at,
                    updated_at,
                    resolved_at,
                    closed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    ticket.ticket_number,
                    ticket.title,
                    ticket.description,
                    ticket.category.value,
                    ticket.priority.value,
                    ticket.status.value,
                    ticket.requester_name,
                    ticket.requester_email,
                    ticket.assigned_to,
                    ticket.resolution,
                    ticket.created_at.isoformat(),
                    ticket.updated_at.isoformat(),
                    (
                        ticket.resolved_at.isoformat()
                        if ticket.resolved_at
                        else None
                    ),
                    (
                        ticket.closed_at.isoformat()
                        if ticket.closed_at
                        else None
                    ),
                ),
            )

            connection.commit()

            ticket.id = cursor.lastrowid

            return ticket

        except sqlite3.IntegrityError as exc:
            if connection is not None:
                connection.rollback()

            raise DatabaseError(
                f"Unable to create ticket: {exc}"
            ) from exc

        except sqlite3.Error as exc:
            if connection is not None:
                connection.rollback()

            raise DatabaseError(
                f"Database error while creating ticket: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()

    def get_by_id(
        self,
        ticket_id: int,
    ) -> Ticket:
        """Retrieve a ticket by its database ID."""

        connection: sqlite3.Connection | None = None

        try:
            connection = self.database.connect()

            row = connection.execute(
                """
                SELECT *
                FROM tickets
                WHERE id = ?;
                """,
                (ticket_id,),
            ).fetchone()

            if row is None:
                raise TicketNotFoundError(
                    f"Ticket with ID {ticket_id} was not found."
                )

            return self._row_to_ticket(row)

        except TicketNotFoundError:
            raise

        except sqlite3.Error as exc:
            raise DatabaseError(
                f"Unable to retrieve ticket: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()

    def get_by_ticket_number(
        self,
        ticket_number: str,
    ) -> Ticket:
        """Retrieve a ticket using its public ticket number."""

        connection: sqlite3.Connection | None = None

        try:
            connection = self.database.connect()

            row = connection.execute(
                """
                SELECT *
                FROM tickets
                WHERE ticket_number = ?;
                """,
                (ticket_number,),
            ).fetchone()

            if row is None:
                raise TicketNotFoundError(
                    f"Ticket {ticket_number} was not found."
                )

            return self._row_to_ticket(row)

        except TicketNotFoundError:
            raise

        except sqlite3.Error as exc:
            raise DatabaseError(
                f"Unable to retrieve ticket: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()

    def list_all(self) -> list[Ticket]:
        """Return all tickets ordered by newest first."""

        connection: sqlite3.Connection | None = None

        try:
            connection = self.database.connect()

            rows = connection.execute(
                """
                SELECT *
                FROM tickets
                ORDER BY id DESC;
                """
            ).fetchall()

            return [
                self._row_to_ticket(row)
                for row in rows
            ]

        except sqlite3.Error as exc:
            raise DatabaseError(
                f"Unable to list tickets: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()

    def search(
        self,
        keyword: str,
    ) -> list[Ticket]:
        """Search tickets by number, title, description, or requester."""

        connection: sqlite3.Connection | None = None

        try:
            connection = self.database.connect()

            search_term = f"%{keyword.strip()}%"

            rows = connection.execute(
                """
                SELECT *
                FROM tickets
                WHERE ticket_number LIKE ?
                   OR title LIKE ?
                   OR description LIKE ?
                   OR requester_name LIKE ?
                   OR requester_email LIKE ?
                ORDER BY id DESC;
                """,
                (
                    search_term,
                    search_term,
                    search_term,
                    search_term,
                    search_term,
                ),
            ).fetchall()

            return [
                self._row_to_ticket(row)
                for row in rows
            ]

        except sqlite3.Error as exc:
            raise DatabaseError(
                f"Unable to search tickets: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()

    def update(
        self,
        ticket: Ticket,
    ) -> Ticket:
        """Persist changes to an existing ticket."""

        if ticket.id is None:
            raise DatabaseError(
                "Cannot update a ticket without a database ID."
            )

        connection: sqlite3.Connection | None = None

        try:
            connection = self.database.connect()

            cursor = connection.execute(
                """
                UPDATE tickets
                SET
                    title = ?,
                    description = ?,
                    category = ?,
                    priority = ?,
                    status = ?,
                    requester_name = ?,
                    requester_email = ?,
                    assigned_to = ?,
                    resolution = ?,
                    updated_at = ?,
                    resolved_at = ?,
                    closed_at = ?
                WHERE id = ?;
                """,
                (
                    ticket.title,
                    ticket.description,
                    ticket.category.value,
                    ticket.priority.value,
                    ticket.status.value,
                    ticket.requester_name,
                    ticket.requester_email,
                    ticket.assigned_to,
                    ticket.resolution,
                    ticket.updated_at.isoformat(),
                    (
                        ticket.resolved_at.isoformat()
                        if ticket.resolved_at
                        else None
                    ),
                    (
                        ticket.closed_at.isoformat()
                        if ticket.closed_at
                        else None
                    ),
                    ticket.id,
                ),
            )

            if cursor.rowcount == 0:
                raise TicketNotFoundError(
                    f"Ticket with ID {ticket.id} was not found."
                )

            connection.commit()

            return ticket

        except TicketNotFoundError:
            if connection is not None:
                connection.rollback()

            raise

        except sqlite3.Error as exc:
            if connection is not None:
                connection.rollback()

            raise DatabaseError(
                f"Unable to update ticket: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()

    def get_next_ticket_number(self) -> str:
        """Generate the next sequential ticket number."""

        connection: sqlite3.Connection | None = None

        try:
            connection = self.database.connect()

            row = connection.execute(
                """
                SELECT ticket_number
                FROM tickets
                ORDER BY id DESC
                LIMIT 1;
                """
            ).fetchone()

            if row is None:
                return "HD-00001"

            last_ticket_number = row["ticket_number"]

            try:
                last_number = int(
                    last_ticket_number.split("-")[1]
                )
            except (IndexError, ValueError) as exc:
                raise DatabaseError(
                    "Existing ticket number format is invalid."
                ) from exc

            return f"HD-{last_number + 1:05d}"

        except DatabaseError:
            raise

        except sqlite3.Error as exc:
            raise DatabaseError(
                f"Unable to generate ticket number: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()

    @staticmethod
    def _row_to_ticket(
        row: sqlite3.Row,
    ) -> Ticket:
        """Convert a SQLite row into a Ticket object."""

        return Ticket(
            id=row["id"],
            ticket_number=row["ticket_number"],
            title=row["title"],
            description=row["description"],
            category=TicketCategory(
                row["category"]
            ),
            priority=TicketPriority(
                row["priority"]
            ),
            status=TicketStatus(
                row["status"]
            ),
            requester_name=row["requester_name"],
            requester_email=row["requester_email"],
            assigned_to=row["assigned_to"],
            resolution=row["resolution"],
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
            updated_at=datetime.fromisoformat(
                row["updated_at"]
            ),
            resolved_at=(
                datetime.fromisoformat(
                    row["resolved_at"]
                )
                if row["resolved_at"]
                else None
            ),
            closed_at=(
                datetime.fromisoformat(
                    row["closed_at"]
                )
                if row["closed_at"]
                else None
            ),
        )
