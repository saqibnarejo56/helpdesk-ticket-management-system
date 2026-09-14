import tempfile
import unittest
from pathlib import Path

from src.database.connection import DatabaseConnection
from src.database.schema import DatabaseSchema


class DatabaseFoundationTests(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()

        self.database_path = (
            Path(self.temp_directory.name)
            / "data"
            / "helpdesk.db"
        )

        self.database = DatabaseConnection(
            self.database_path
        )

        self.schema = DatabaseSchema(
            self.database
        )

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_connection_creates_database_file(self) -> None:
        connection = self.database.connect()
        connection.close()

        self.assertTrue(
            self.database_path.exists()
        )

    def test_connection_test_returns_true(self) -> None:
        self.assertTrue(
            self.database.test_connection()
        )

    def test_foreign_keys_are_enabled(self) -> None:
        connection = self.database.connect()

        try:
            result = connection.execute(
                "PRAGMA foreign_keys;"
            ).fetchone()

            self.assertIsNotNone(
                result
            )

            self.assertEqual(
                result[0],
                1,
            )

        finally:
            connection.close()

    def test_schema_verify_is_false_before_creation(
        self,
    ) -> None:
        self.assertFalse(
            self.schema.verify()
        )

    def test_schema_create_and_verify(self) -> None:
        self.schema.create()

        self.assertTrue(
            self.schema.verify()
        )

    def test_required_tables_exist(self) -> None:
        self.schema.create()

        connection = self.database.connect()

        try:
            rows = connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table';
                """
            ).fetchall()

            tables = {
                row["name"]
                for row in rows
            }

            self.assertIn(
                "tickets",
                tables,
            )

            self.assertIn(
                "ticket_history",
                tables,
            )

        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
