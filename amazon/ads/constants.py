"""Constants for Amazon Advertising API integration."""

AMAZON_ADS_DEFAULT_API_BASE_URL = "https://advertising-api.amazon.com"
AMAZON_ADS_DEFAULT_TOKEN_URL = "https://api.amazon.com/auth/o2/token"
AMAZON_LWA_AUTHORIZATION_URL = "https://www.amazon.com/ap/oa"

AMAZON_ADS_PROFILES_PATH = "/v2/profiles"

AMAZON_ADS_CLIENT_ID_HEADER = "Amazon-Advertising-API-ClientId"
AUTHORIZATION_HEADER = "Authorization"
CONTENT_TYPE_HEADER = "Content-Type"
JSON_CONTENT_TYPE = "application/json"

OAUTH_REFRESH_GRANT_TYPE = "refresh_token"
OAUTH_AUTHORIZATION_CODE_GRANT_TYPE = "authorization_code"
OAUTH_RESPONSE_TYPE_CODE = "code"
AMAZON_ADS_OAUTH_SCOPE = "advertising::campaign_management"
TOKEN_EXPIRY_SAFETY_SECONDS = 60
