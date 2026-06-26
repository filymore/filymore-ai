"""Advertising profile operations for Amazon Ads."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from amazon.ads.client import AmazonAdsClient
from amazon.ads.constants import AMAZON_ADS_PROFILES_PATH
from amazon.ads.errors import AmazonAdsApiError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AmazonAdsProfile:
    """Safe, non-secret advertising profile summary."""

    profile_id: str
    country_code: str | None
    account_id: str | None
    account_name: str | None
    account_type: str | None


class AmazonAdsProfilesService:
    """Profile-related Amazon Ads API operations."""

    def __init__(self, client: AmazonAdsClient) -> None:
        self._client = client

    def list_profiles(self) -> list[AmazonAdsProfile]:
        """List advertising profiles available to the authenticated account."""

        logger.info("Listing Amazon Ads advertising profiles")
        data = self._client.get(AMAZON_ADS_PROFILES_PATH)

        if not isinstance(data, list):
            raise AmazonAdsApiError("Amazon Ads profiles response was not a list")

        profiles = [self._parse_profile(item) for item in data]
        logger.info("Found %s Amazon Ads advertising profiles", len(profiles))
        return profiles

    @staticmethod
    def _parse_profile(item: Any) -> AmazonAdsProfile:
        if not isinstance(item, dict):
            raise AmazonAdsApiError("Amazon Ads profile item was not an object")

        account_info = item.get("accountInfo")
        if not isinstance(account_info, dict):
            account_info = {}

        profile_id = item.get("profileId")
        if profile_id is None:
            raise AmazonAdsApiError("Amazon Ads profile item did not include profileId")

        return AmazonAdsProfile(
            profile_id=str(profile_id),
            country_code=_optional_string(item.get("countryCode")),
            account_id=_optional_string(account_info.get("id")),
            account_name=_optional_string(account_info.get("name")),
            account_type=_optional_string(account_info.get("type")),
        )


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)
