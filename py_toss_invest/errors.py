"""
Exception classes for Toss Invest API client.
"""


class TossInvestError(Exception):
    """Base exception for all Toss Invest API errors."""

    pass


class AuthenticationError(TossInvestError):
    """Raised when authentication fails."""

    pass


class TokenExpiredError(AuthenticationError):
    """Raised when the access token has expired."""

    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when credentials (client_id/client_secret) are invalid."""

    pass


class APIError(TossInvestError):
    """Raised when API returns an error response."""

    def __init__(self, code: str, message: str, request_id: str = None, data: dict = None):
        self.code = code
        self.message = message
        self.request_id = request_id
        self.data = data or {}
        super().__init__(
            f"{code}: {message}" + (f" (Request ID: {request_id})" if request_id else "")
        )


class RateLimitExceededError(APIError):
    """Raised when rate limit is exceeded."""

    pass


class NotFoundError(APIError):
    """Raised when requested resource is not found."""

    pass


class ValidationError(TossInvestError):
    """Raised when request validation fails."""

    pass


class NetworkError(TossInvestError):
    """Raised when network error occurs."""

    pass
