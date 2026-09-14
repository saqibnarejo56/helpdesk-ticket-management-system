import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.exceptions.exceptions import ConfigurationError


LOGGER_NAME = "helpdesk"


def configure_logging(
    log_file: Path | str,
    log_level: str = "INFO",
) -> logging.Logger:
    """Configure application file logging."""

    log_path = Path(log_file)

    level_name = log_level.strip().upper()

    level = getattr(
        logging,
        level_name,
        None,
    )

    if not isinstance(level, int):
        raise ConfigurationError(
            f"Invalid logging level: {log_level}"
        )

    try:
        log_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
    except OSError as exc:
        raise ConfigurationError(
            f"Unable to create log directory: {exc}"
        ) from exc

    logger = logging.getLogger(
        LOGGER_NAME
    )

    logger.setLevel(
        level
    )

    logger.propagate = False

    for handler in logger.handlers[:]:
        logger.removeHandler(
            handler
        )

        handler.close()

    try:
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
    except OSError as exc:
        raise ConfigurationError(
            f"Unable to open log file: {exc}"
        ) from exc

    file_handler.setLevel(
        level
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    return logger
