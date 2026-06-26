"""HTTP client wrapper for Amazon Advertising API calls."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from amazon.ads.errors import AmazonAdsApiError

logger = logging.getLogger(__name__)


class AmazonAdsClient:
    """Small Amazon Ads API wrapper around an injected authenticated HTTP client."""

    def __init__(self, http_client: httpx.Client) -> None:
        self._http_client = http_client

    def get(self, path: str) -> Any:
        """Perform a GET request and return parsed JSON."""

        logger.info("Sending Amazon Ads GET request to %s", path)

        try:
            response = self._http_client.get(path)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            raise AmazonAdsApiError(
                f"Amazon Ads API GET {path} failed with status {status_code}",
                status_code=status_code,
            ) from exc
        except httpx.HTTPError as exc:
            raise AmazonAdsApiError(f"Amazon Ads API GET {path} failed") from exc

        try:
            return response.json()
        except ValueError as exc:
            raise AmazonAdsApiError(f"Amazon Ads API GET {path} returned invalid JSON") from exc
