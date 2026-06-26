"""OAuth authentication for Amazon Advertising API."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

import httpx
from pydantic import SecretStr

from amazon.ads.constants import (
    AUTHORIZATION_HEADER,
    OAUTH_REFRESH_GRANT_TYPE,
    TOKEN_EXPIRY_SAFETY_SECONDS,
)
from amazon.ads.errors import AmazonAdsAuthError, AmazonAdsConfigError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AccessToken:
    """In-memory OAuth access token metadata."""

    value: str
    expires_at: float

    def is_valid(self) -> bool:
        """Return whether the token is valid beyond the safety window."""

        return time.time() < self.expires_at - TOKEN_EXPIRY_SAFETY_SECONDS


class AmazonAdsAuthenticator:
    """Refreshes and supplies Amazon Ads OAuth access tokens."""

    def __init__(
        self,
        *,
        client_id: str | None,
        client_secret: SecretStr | None,
        refresh_token: SecretStr | None,
        token_url: str,
        timeout_seconds: float,
    ) -> None:
        self._client_id = self._require_value(client_id, "AMAZON_ADS_CLIENT_ID")
        self._client_secret = self._require_secret(
            client_secret,
            "AMAZON_ADS_CLIENT_SECRET",
        )
        self._refresh_token = self._require_secret(
            refresh_token,
            "AMAZON_ADS_REFRESH_TOKEN",
        )
        self._token_url = token_url
        self._timeout_seconds = timeout_seconds
        self._access_token: AccessToken | None = None

    @property
    def client_id(self) -> str:
        """Return the non-secret Amazon Ads client ID."""

        return self._client_id

    def get_access_token(self) -> str:
        """Return a valid access token, refreshing it when needed."""

        if self._access_token and self._access_token.is_valid():
            return self._access_token.value

        self._access_token = self._refresh_access_token()
        return self._access_token.value

    def as_httpx_auth(self) -> httpx.Auth:
        """Return an httpx auth adapter backed by this authenticator."""

        return _AmazonAdsHttpxAuth(self)

    def _refresh_access_token(self) -> AccessToken:
        logger.info("Refreshing Amazon Ads OAuth access token")

        payload = {
            "grant_type": OAUTH_REFRESH_GRANT_TYPE,
            "refresh_token": self._refresh_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }

        try:
            response = httpx.post(
                self._token_url,
                data=payload,
                timeout=self._timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            raise AmazonAdsAuthError(
                f"Amazon Ads OAuth token refresh failed with status {status_code}"
            ) from exc
        except httpx.HTTPError as exc:
            raise AmazonAdsAuthError("Amazon Ads OAuth token refresh failed") from exc

        token_data = response.json()
        access_token = token_data.get("access_token")
        expires_in = token_data.get("expires_in")

        if not isinstance(access_token, str) or not access_token:
            raise AmazonAdsAuthError("Amazon Ads OAuth response did not include an access token")
        if not isinstance(expires_in, int | float) or expires_in <= 0:
            raise AmazonAdsAuthError("Amazon Ads OAuth response did not include a valid expiry")

        logger.info("Amazon Ads OAuth access token refreshed")
        return AccessToken(
            value=access_token,
            expires_at=time.time() + float(expires_in),
        )

    @staticmethod
    def _require_value(value: str | None, name: str) -> str:
        if value:
            return value
        raise AmazonAdsConfigError(f"{name} is required for Amazon Ads authentication")

    @staticmethod
    def _require_secret(value: SecretStr | None, name: str) -> str:
        if value and value.get_secret_value():
            return value.get_secret_value()
        raise AmazonAdsConfigError(f"{name} is required for Amazon Ads authentication")


class _AmazonAdsHttpxAuth(httpx.Auth):
    """httpx authentication adapter for Amazon Ads OAuth."""

    def __init__(self, authenticator: AmazonAdsAuthenticator) -> None:
        self._authenticator = authenticator

    def auth_flow(self, request: httpx.Request) -> httpx.Request:
        request.headers[AUTHORIZATION_HEADER] = (
            f"Bearer {self._authenticator.get_access_token()}"
        )
        yield request
