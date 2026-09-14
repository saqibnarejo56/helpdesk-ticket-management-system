class HelpdeskError(Exception):
    """Base exception for the helpdesk application."""


class ConfigurationError(HelpdeskError):
    """Raised when application configuration is missing or invalid."""


class DatabaseError(HelpdeskError):
    """Raised when a database operation fails."""


class ValidationError(HelpdeskError):
    """Raised when user input or application data is invalid."""


class TicketNotFoundError(HelpdeskError):
    """Raised when the requested ticket does not exist."""


class InvalidStatusTransitionError(HelpdeskError):
    """Raised when a ticket status change is not allowed."""
