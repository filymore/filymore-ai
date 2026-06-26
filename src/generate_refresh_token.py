"""One-time Login with Amazon refresh token generator."""

from __future__ import annotations

import secrets
import sys
from pathlib import Path
from urllib.parse import urlencode

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import httpx
from pydantic import SecretStr, ValidationError

from amazon.ads.constants import (
    AMAZON_ADS_OAUTH_SCOPE,
    AMAZON_LWA_AUTHORIZATION_URL,
    OAUTH_AUTHORIZATION_CODE_GRANT_TYPE,
    OAUTH_RESPONSE_TYPE_CODE,
)
from amazon.ads.errors import AmazonAdsAuthError, AmazonAdsConfigError
from config import get_settings


def main() -> int:
    """Generate an Amazon Ads refresh token from an authorization code."""

    try:
        settings = get_settings()
        client_id = _require_value(settings.amazon_ads_client_id, "AMAZON_ADS_CLIENT_ID")
        client_secret = _require_secret(
            settings.amazon_ads_client_secret,
            "AMAZON_ADS_CLIENT_SECRET",
        )
        redirect_uri = _require_value(
            settings.amazon_ads_redirect_uri,
            "AMAZON_ADS_REDIRECT_URI",
        )
    except (AmazonAdsConfigError, ValidationError) as exc:
        print(f"Configuration error: {_safe_error_message(exc)}", file=sys.stderr)
        return 1

    state = secrets.token_urlsafe(24)
    authorization_url = _build_authorization_url(
        client_id=client_id,
        redirect_uri=redirect_uri,
        state=state,
    )

    print("Open this Login with Amazon authorization URL:")
    print(authorization_url)
    print()
    print("After authorization, paste the returned authorization code.")
    authorization_code = input("Authorization code: ").strip()

    if not authorization_code:
        print("Authorization code is required.", file=sys.stderr)
        return 1

    try:
        refresh_token = _exchange_authorization_code(
            authorization_code=authorization_code,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            token_url=settings.amazon_ads_token_url,
            timeout_seconds=settings.amazon_ads_request_timeout_seconds,
        )
    except AmazonAdsAuthError as exc:
        print(f"Token exchange failed: {exc}", file=sys.stderr)
        return 1

    print(refresh_token)
    return 0


def _build_authorization_url(*, client_id: str, redirect_uri: str, state: str) -> str:
    query = urlencode(
        {
            "client_id": client_id,
            "scope": AMAZON_ADS_OAUTH_SCOPE,
            "response_type": OAUTH_RESPONSE_TYPE_CODE,
            "redirect_uri": redirect_uri,
            "state": state,
        },
    )
    return f"{AMAZON_LWA_AUTHORIZATION_URL}?{query}"


def _exchange_authorization_code(
    *,
    authorization_code: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    token_url: str,
    timeout_seconds: float,
) -> str:
    payload = {
        "grant_type": OAUTH_AUTHORIZATION_CODE_GRANT_TYPE,
        "code": authorization_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }

    try:
        response = httpx.post(token_url, data=payload, timeout=timeout_seconds)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        raise AmazonAdsAuthError(
            f"Login with Amazon token endpoint returned status {status_code}"
        ) from exc
    except httpx.HTTPError as exc:
        raise AmazonAdsAuthError("Login with Amazon token request failed") from exc

    try:
        token_data = response.json()
    except ValueError as exc:
        raise AmazonAdsAuthError("Token response returned invalid JSON") from exc

    refresh_token = token_data.get("refresh_token")

    if not isinstance(refresh_token, str) or not refresh_token:
        raise AmazonAdsAuthError("Token response did not include a refresh token")

    return refresh_token


def _require_value(value: str | None, name: str) -> str:
    if value:
        return value
    raise AmazonAdsConfigError(f"{name} is required")


def _require_secret(value: SecretStr | None, name: str) -> str:
    if value and value.get_secret_value():
        return value.get_secret_value()
    raise AmazonAdsConfigError(f"{name} is required")


def _safe_error_message(exc: Exception) -> str:
    if isinstance(exc, ValidationError):
        fields = []
        for error in exc.errors(include_input=False):
            location = ".".join(str(part) for part in error["loc"])
            fields.append(f"{location}: {error['msg']}")
        return "; ".join(fields)

    return str(exc)


if __name__ == "__main__":
    raise SystemExit(main())
