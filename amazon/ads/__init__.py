"""Amazon Advertising API integration package."""

from amazon.ads.auth import AmazonAdsAuthenticator
from amazon.ads.client import AmazonAdsClient
from amazon.ads.profiles import AmazonAdsProfile, AmazonAdsProfilesService

__all__ = [
    "AmazonAdsAuthenticator",
    "AmazonAdsClient",
    "AmazonAdsProfile",
    "AmazonAdsProfilesService",
]
