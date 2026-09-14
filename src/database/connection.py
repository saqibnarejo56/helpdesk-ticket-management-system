import sqlite3
from pathlib import Path

from src.exceptions.exceptions import DatabaseError


class DatabaseConnection:
    """Manages SQLite database connections for the helpdesk system."""

    def __init__(self, database_path: Path | str) -> None:
        self.database_path = Path(database_path)

    def connect(self) -> sqlite3.Connection:
        """Create and configure a SQLite database connection."""

        try:
            self.database_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            connection = sqlite3.connect(
                self.database_path,
                timeout=10.0,
            )

            connection.row_factory = sqlite3.Row

            connection.execute(
                "PRAGMA foreign_keys = ON;"
            )

            return connection

        except (sqlite3.Error, OSError) as exc:
            raise DatabaseError(
                f"Unable to connect to the database: {exc}"
            ) from exc

    def test_connection(self) -> bool:
        """Verify that the SQLite database can be opened and queried."""

        connection: sqlite3.Connection | None = None

        try:
            connection = self.connect()

            cursor = connection.execute(
                "SELECT 1;"
            )

            result = cursor.fetchone()

            return result is not None and result[0] == 1

        except sqlite3.Error as exc:
            raise DatabaseError(
                f"Database connection test failed: {exc}"
            ) from exc

        finally:
            if connection is not None:
                connection.close()
