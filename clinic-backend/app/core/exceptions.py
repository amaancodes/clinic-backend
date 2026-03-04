class DomainError(Exception):
    """Base class for domain-specific errors."""


class AuthenticationError(DomainError):
    """Raised when authentication fails (e.g., invalid credentials)."""


class AuthorizationError(DomainError):
    """Raised when a user is not authorized to perform an action."""


class ResourceNotFoundError(DomainError):
    """Raised when a requested resource cannot be found."""


class ConflictError(DomainError):
    """Raised when a resource conflict occurs (e.g., duplicate unique value)."""


class ValidationError(DomainError):
    """Raised when input data fails validation rules."""

class ClinicException(Exception):
    status_code = 400

    def __init__(self, message):
        self.message = message

