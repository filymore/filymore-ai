# Amazon Ads Authentication

Filymore OS uses Amazon Advertising OAuth credentials to refresh access tokens and call the Amazon Ads API.

## Required Environment Variables

Add these values to your local `.env` file:

```text
AMAZON_ADS_CLIENT_ID=
AMAZON_ADS_CLIENT_SECRET=
AMAZON_ADS_REFRESH_TOKEN=
AMAZON_ADS_REDIRECT_URI=
AMAZON_ADS_API_BASE_URL=https://advertising-api.amazon.com
AMAZON_ADS_TOKEN_URL=https://api.amazon.com/auth/o2/token
AMAZON_ADS_REQUEST_TIMEOUT_SECONDS=30
```

Do not commit real credential values.

## Architecture

- `amazon/ads/auth.py` refreshes OAuth access tokens.
- `amazon/ads/client.py` performs authenticated HTTP requests through an injected HTTP client.
- `amazon/ads/profiles.py` lists available advertising profiles.
- `amazon/ads/constants.py` contains Amazon Ads URLs, headers, paths, and integration constants.
- `src/main.py` runs the connection test.
- `src/generate_refresh_token.py` runs the one-time refresh token generation flow.

## Generate Refresh Token

Set these values in `.env` before running the utility:

```text
AMAZON_ADS_CLIENT_ID=
AMAZON_ADS_CLIENT_SECRET=
AMAZON_ADS_REDIRECT_URI=
```

The redirect URI must match the URI configured in your Login with Amazon security profile.

Run:

```powershell
python src/generate_refresh_token.py
```

The utility prints a Login with Amazon authorization URL, prompts for the returned authorization code, exchanges it for tokens, and displays only the refresh token.

The utility does not save the refresh token to `.env`.

## Connection Test

Run:

```powershell
python src/main.py
```

The command refreshes an access token and lists available advertising profiles. Logs include only safe, non-secret information.

## Not Included Yet

- Dashboard features
- Campaign downloads
- Amazon SP-API integration
- AWS role authentication
