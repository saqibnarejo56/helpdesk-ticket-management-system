import json
from pathlib import Path
from typing import Any

from src.exceptions.exceptions import ConfigurationError


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "settings.json"


class ConfigLoader:
    REQUIRED_SECTIONS = (
        "application",
        "database",
        "logging",
    )

    VALID_LOG_LEVELS = {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }

    def __init__(
        self,
        config_path: Path | str = DEFAULT_CONFIG_PATH,
    ) -> None:
        self.config_path = Path(config_path)
        self._config: dict[str, Any] = {}

    def load(self) -> dict[str, Any]:
        if not self.config_path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {self.config_path}"
            )

        if not self.config_path.is_file():
            raise ConfigurationError(
                f"Configuration path is not a file: {self.config_path}"
            )

        try:
            with self.config_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                config = json.load(file)

        except json.JSONDecodeError as exc:
            raise ConfigurationError(
                f"Invalid JSON configuration: {exc}"
            ) from exc

        except OSError as exc:
            raise ConfigurationError(
                f"Unable to read configuration file: {exc}"
            ) from exc

        if not isinstance(config, dict):
            raise ConfigurationError(
                "Configuration root must be a JSON object."
            )

        self._validate(config)
        self._config = config

        return self._config.copy()

    def _validate(
        self,
        config: dict[str, Any],
    ) -> None:
        for section in self.REQUIRED_SECTIONS:
            if section not in config:
                raise ConfigurationError(
                    f"Missing configuration section: {section}"
                )

            if not isinstance(config[section], dict):
                raise ConfigurationError(
                    f"Configuration section '{section}' "
                    "must be an object."
                )

        self._validate_application(
            config["application"]
        )

        self._validate_database(
            config["database"]
        )

        self._validate_logging(
            config["logging"]
        )

    @staticmethod
    def _validate_application(
        application: dict[str, Any],
    ) -> None:
        required_fields = (
            "name",
            "version",
            "environment",
        )

        for field in required_fields:
            value = application.get(field)

            if not isinstance(value, str) or not value.strip():
                raise ConfigurationError(
                    f"Invalid application configuration: '{field}'"
                )

    @staticmethod
    def _validate_database(
        database: dict[str, Any],
    ) -> None:
        database_path = database.get("path")

        if (
            not isinstance(database_path, str)
            or not database_path.strip()
        ):
            raise ConfigurationError(
                "Database path must be a non-empty string."
            )

    def _validate_logging(
        self,
        logging_config: dict[str, Any],
    ) -> None:
        log_level = logging_config.get("level")
        log_file = logging_config.get("file")

        if (
            not isinstance(log_level, str)
            or log_level.upper() not in self.VALID_LOG_LEVELS
        ):
            raise ConfigurationError(
                "Invalid logging level."
            )

        if (
            not isinstance(log_file, str)
            or not log_file.strip()
        ):
            raise ConfigurationError(
                "Logging file path must be a non-empty string."
            )

    def get_database_path(self) -> Path:
        self._ensure_loaded()

        return (
            PROJECT_ROOT
            / self._config["database"]["path"]
        ).resolve()

    def get_log_file_path(self) -> Path:
        self._ensure_loaded()

        return (
            PROJECT_ROOT
            / self._config["logging"]["file"]
        ).resolve()

    def get_log_level(self) -> str:
        self._ensure_loaded()

        return self._config["logging"]["level"].upper()

    def get_application_name(self) -> str:
        self._ensure_loaded()

        return self._config["application"]["name"]

    def _ensure_loaded(self) -> None:
        if not self._config:
            raise ConfigurationError(
                "Configuration has not been loaded yet."
            )
