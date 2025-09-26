"""
Custom exceptions for the application
"""


class ValidationError(Exception):
    """Raised when validation fails"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(Exception):
    """Raised when user is not found"""
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)


class AuthorizationError(Exception):
    """Raised when user is not authorized to perform an action"""
    def __init__(self, message: str = "Not authorized"):
        self.message = message
        super().__init__(self.message)

