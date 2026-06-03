"""
Authentication-related dataclasses.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class OAuth2TokenResponse:
    """
    OAuth2 token response from /oauth2/token endpoint.

    Attributes:
        access_token: The access token string to be used in Authorization header
        token_type: Token type (usually "Bearer")
        expires_in: Token expiration time in seconds
        scope: Space-separated list of granted scopes (optional)
    """

    access_token: str
    token_type: str
    expires_in: int
    scope: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "OAuth2TokenResponse":
        """Create OAuth2TokenResponse from dictionary response."""
        return cls(
            access_token=data.get("access_token"),
            token_type=data.get("token_type"),
            expires_in=data.get("expires_in"),
            scope=data.get("scope"),
        )
