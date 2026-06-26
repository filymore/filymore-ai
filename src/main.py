"""Command-line connection check for Filymore OS."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import httpx
from pydantic import ValidationError

from amazon.ads import AmazonAdsAuthenticator, AmazonAdsClient, AmazonAdsProfilesService
from amazon.ads.constants import AMAZON_ADS_CLIENT_ID_HEADER
from amazon.ads.errors import AmazonAdsError
from config import configure_logging, get_settings

logger = logging.getLogger(__name__)


def main() -> int:
    """Run the Amazon Ads profile-listing connection check."""

    try:
        settings = get_settings()
    except ValidationError as exc:
        logging.basicConfig(
            level=logging.ERROR,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logger.error("Configuration validation failed: %s", _format_validation_errors(exc))
        return 1

    configure_logging(settings)

    logger.info("Starting Amazon Ads connection test")

    try:
        authenticator = AmazonAdsAuthenticator(
            client_id=settings.amazon_ads_client_id,
            client_secret=settings.amazon_ads_client_secret,
            refresh_token=settings.amazon_ads_refresh_token,
            token_url=settings.amazon_ads_token_url,
            timeout_seconds=settings.amazon_ads_request_timeout_seconds,
        )

        with httpx.Client(
            base_url=settings.amazon_ads_api_base_url,
            timeout=settings.amazon_ads_request_timeout_seconds,
            headers={AMAZON_ADS_CLIENT_ID_HEADER: authenticator.client_id},
            auth=authenticator.as_httpx_auth(),
        ) as http_client:
            ads_client = AmazonAdsClient(http_client)
            profiles_service = AmazonAdsProfilesService(ads_client)
            profiles = profiles_service.list_profiles()

        for profile in profiles:
            logger.info(
                "Profile %s | country=%s | account_id=%s | account_name=%s | account_type=%s",
                profile.profile_id,
                profile.country_code or "unknown",
                profile.account_id or "unknown",
                profile.account_name or "unknown",
                profile.account_type or "unknown",
            )

        logger.info("Amazon Ads connection test completed successfully")
        return 0
    except AmazonAdsError as exc:
        logger.error("Amazon Ads connection test failed: %s", exc)
        return 1


def _format_validation_errors(exc: ValidationError) -> str:
    """Return a safe summary of configuration validation errors."""

    fields = []
    for error in exc.errors(include_input=False):
        location = ".".join(str(part) for part in error["loc"])
        message = error["msg"]
        fields.append(f"{location}: {message}")

    return "; ".join(fields)


if __name__ == "__main__":
    raise SystemExit(main())
