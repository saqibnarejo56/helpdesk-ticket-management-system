import logging

from src.config.config_loader import ConfigLoader
from src.database.connection import DatabaseConnection
from src.database.schema import DatabaseSchema
from src.logging_setup import configure_logging
from src.repositories.ticket_history_repository import (
    TicketHistoryRepository,
)
from src.repositories.ticket_repository import TicketRepository
from src.services.ticket_service import TicketService


class HelpdeskApplication:
    """Builds and owns the core helpdesk application services."""

    def __init__(self) -> None:
        self.config = ConfigLoader()
        self.logger: logging.Logger | None = None
        self.ticket_service: TicketService | None = None

    def initialize(self) -> None:
        """Initialize configuration, logging, database, and services."""

        self.config.load()

        self.logger = configure_logging(
            self.config.get_log_file_path(),
            self.config.get_log_level(),
        )

        self.logger.info(
            "Starting %s.",
            self.config.get_application_name(),
        )

        database = DatabaseConnection(
            self.config.get_database_path()
        )

        schema = DatabaseSchema(
            database
        )

        schema.create()

        if not schema.verify():
            raise RuntimeError(
                "Database schema verification failed."
            )

        ticket_repository = TicketRepository(
            database
        )

        history_repository = TicketHistoryRepository(
            database
        )

        self.ticket_service = TicketService(
            ticket_repository,
            history_repository,
        )

        self.logger.info(
            "Application initialization completed successfully."
        )

    def get_ticket_service(self) -> TicketService:
        """Return the initialized ticket service."""

        if self.ticket_service is None:
            raise RuntimeError(
                "Application has not been initialized."
            )

        return self.ticket_service
