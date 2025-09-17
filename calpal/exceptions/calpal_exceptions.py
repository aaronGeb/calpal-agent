"""
CalPal Custom Exceptions
"""


class CalPalException(Exception):
    """Base exception for CalPal"""
    pass


class ParsingError(CalPalException):
    """Raised when natural language parsing fails"""
    pass


class CalendarError(CalPalException):
    """Raised when calendar operations fail"""
    pass


class AuthenticationError(CalPalException):
    """Raised when authentication fails"""
    pass


class ConfigurationError(CalPalException):
    """Raised when configuration is invalid"""
    pass

