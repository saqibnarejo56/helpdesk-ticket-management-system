import sqlite3

from src.database.connection import DatabaseConnection
from src.exceptions.exceptions import DatabaseError


class DatabaseSchema:
    """Creates and verifies the database schema for the helpdesk system."""

    REQUIRED_TABLES = {
        "tickets",
        "ticket_history",
    }

    def __init__(
        self,
        database: DatabaseConnection,
    ) -> None:
        self.database = database

    def create(self) -> None:
        """Create all required database tables and indexes."""

        connection: sqlite3.Connection | None = None

        try:
            connection = self.database.connect()

            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    ticket_number TEXT NOT NULL UNIQUE,

                    title TEXT NOT NULL,

                    description TEXT NOT NULL,

                    category TEXT NOT NULL
                        CHECK (
                            category IN (
                                'Hardware',
                                'Software',
                                'Network',
                                'Email',
                                'Access',
                                'Printer',
                                'Other'
                            )
                        ),

                    priority TEXT NOT NULL
                        DEFAULT 'MEDIUM'
                        CHECK (
                            priority IN (
                                'LOW',
                                'MEDIUM',
                                'HIGH',
                                'CRITICAL'
                            )
                        ),

                    status TEXT NOT NULL
                        DEFAULT 'OPEN'
                        CHECK (
                            status IN (
                                'OPEN',
                                'IN_PROGRESS',
                                'RESOLVED',
                                'CLOSED'
                            )
                        ),

                    requester_name TEXT NOT NULL,

                    requester_email TEXT NOT NULL,

                    assigned_to TEXT,

                    resolution TEXT,

                    created_at TEXT NOT NULL,

                    updated_at TEXT NOT NULL,

                    resolved_at TEXT,

                    closed_at TEXT
                );


                CREATE TABLE IF NOT EXISTS ticket_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    ticket_id INTEGER NOT NULL,

                    action TEXT NOT NULL,

                    field_name TEXT,

                    old_value TEXT,

                    new_value TEXT,

                    changed_at TEXT NOT NULL,

                    FOREIGN KEY (ticket_id)
                        REFERENCES tickets(id)
                        ON DELETE CASCADE
                );


                CREATE INDEX IF NOT EXISTS
                    idx_tickets_ticket_number
                ON tickets(ticket_number);


                CREATE INDEX IF NOT EXISTS
                    idx_tickets_status
                ON tickets(status);


                CREATE INDEX IF NOT EXISTS
                    idx_tickets_priority
                ON tickets(priority);


                CREATE INDEX IF NOT EXISTS
                    idx_tickets_category
                ON tickets(category);


                CREATE INDEX IF NOT EXISTS
                    idx_ticket_history_ticket_id
                ON ticket_history(ticket_id);
                """
            )

            connection.commit()

        except sqlite3.Error as exc:
            if connection is not None:
                connection.rollback()

            raise DatabaseError(
                f"Unable to create database schema: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()

    def verify(self) -> bool:
        """Verify that all required application tables exist."""

        connection: sqlite3.Connection | None = None

        try:
            connection = self.database.connect()

            rows = connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table';
                """
            ).fetchall()

            existing_tables = {
                row["name"]
                for row in rows
            }

            return self.REQUIRED_TABLES.issubset(
                existing_tables
            )

        except sqlite3.Error as exc:
            raise DatabaseError(
                f"Unable to verify database schema: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()
