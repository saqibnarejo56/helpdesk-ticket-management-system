import logging
import tempfile
import unittest
from pathlib import Path

from src.exceptions.exceptions import ConfigurationError
from src.logging_setup import (
    LOGGER_NAME,
    configure_logging,
)


class LoggingSetupTests(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()

        self.temp_path = Path(
            self.temp_directory.name
        )

    def tearDown(self) -> None:
        logger = logging.getLogger(
            LOGGER_NAME
        )

        for handler in logger.handlers[:]:
            logger.removeHandler(
                handler
            )

            handler.close()

        self.temp_directory.cleanup()

    def test_logging_creates_log_file(self) -> None:
        log_file = (
            self.temp_path
            / "logs"
            / "helpdesk.log"
        )

        logger = configure_logging(
            log_file,
            "INFO",
        )

        logger.info(
            "Logging test message."
        )

        for handler in logger.handlers:
            handler.flush()

        self.assertTrue(
            log_file.exists()
        )

        content = log_file.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Logging test message.",
            content,
        )

    def test_logging_creates_missing_directory(self) -> None:
        log_file = (
            self.temp_path
            / "nested"
            / "logs"
            / "helpdesk.log"
        )

        configure_logging(
            log_file,
            "INFO",
        )

        self.assertTrue(
            log_file.parent.exists()
        )

        self.assertTrue(
            log_file.exists()
        )

    def test_invalid_log_level_is_rejected(self) -> None:
        log_file = (
            self.temp_path
            / "helpdesk.log"
        )

        with self.assertRaises(
            ConfigurationError
        ):
            configure_logging(
                log_file,
                "INVALID",
            )

    def test_reconfiguration_does_not_duplicate_handlers(
        self,
    ) -> None:
        log_file = (
            self.temp_path
            / "helpdesk.log"
        )

        logger = configure_logging(
            log_file,
            "INFO",
        )

        configure_logging(
            log_file,
            "DEBUG",
        )

        self.assertEqual(
            len(logger.handlers),
            1,
        )

        self.assertEqual(
            logger.level,
            logging.DEBUG,
        )


if __name__ == "__main__":
    unittest.main()
