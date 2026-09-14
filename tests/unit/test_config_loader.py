import json
import tempfile
import unittest
from pathlib import Path

from src.config.config_loader import ConfigLoader
from src.exceptions.exceptions import ConfigurationError


class ConfigLoaderTests(unittest.TestCase):
    def create_config(self, data: dict) -> Path:
        temp_file = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
            encoding="utf-8",
        )

        json.dump(data, temp_file)
        temp_file.close()

        path = Path(temp_file.name)

        self.addCleanup(
            lambda: path.unlink(missing_ok=True)
        )

        return path

    @staticmethod
    def valid_config() -> dict:
        return {
            "application": {
                "name": "Helpdesk Ticket Management System",
                "version": "1.0.0",
                "environment": "test",
            },
            "database": {
                "path": "data/helpdesk.db",
            },
            "logging": {
                "level": "INFO",
                "file": "logs/helpdesk.log",
            },
        }

    def test_load_valid_configuration(self) -> None:
        path = self.create_config(
            self.valid_config()
        )

        loader = ConfigLoader(path)
        config = loader.load()

        self.assertEqual(
            config["application"]["name"],
            "Helpdesk Ticket Management System",
        )

    def test_missing_configuration_file(self) -> None:
        loader = ConfigLoader(
            "missing-settings.json"
        )

        with self.assertRaises(ConfigurationError):
            loader.load()

    def test_missing_database_section(self) -> None:
        config = self.valid_config()
        del config["database"]

        path = self.create_config(config)
        loader = ConfigLoader(path)

        with self.assertRaises(ConfigurationError):
            loader.load()

    def test_invalid_log_level(self) -> None:
        config = self.valid_config()
        config["logging"]["level"] = "INVALID"

        path = self.create_config(config)
        loader = ConfigLoader(path)

        with self.assertRaises(ConfigurationError):
            loader.load()


if __name__ == "__main__":
    unittest.main()
