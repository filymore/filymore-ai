"""Typed errors for Amazon Advertising API integration."""


class AmazonAdsError(Exception):
    """Base error for Amazon Advertising API integration."""


class AmazonAdsConfigError(AmazonAdsError):
    """Raised when Amazon Ads configuration is missing or invalid."""


class AmazonAdsAuthError(AmazonAdsError):
    """Raised when Amazon Ads OAuth authentication fails."""


class AmazonAdsApiError(AmazonAdsError):
    """Raised when an Amazon Ads API request fails."""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
