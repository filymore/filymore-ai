# Filymore OS

Production-ready Python project scaffold for Filymore OS.

## Project Structure

```text
Filymore-OS/
|-- amazon/
|   |-- __init__.py
|   `-- ads/
|       |-- __init__.py
|       |-- auth.py
|       |-- client.py
|       |-- constants.py
|       |-- errors.py
|       `-- profiles.py
|-- config/
|   |-- __init__.py
|   |-- logging.py
|   `-- settings.py
|-- dashboard/
|-- data/
|   |-- processed/
|   `-- raw/
|-- database/
|-- docs/
|-- logs/
|-- scripts/
|-- src/
|   |-- __init__.py
|   `-- main.py
|-- storage/
|-- tests/
|-- .env.example
|-- .gitignore
|-- PROJECT_ROADMAP.md
|-- README.md
`-- requirements.txt
```

## Status

Filymore OS currently contains the project scaffold, configuration foundation, logging setup, and Amazon Advertising authentication foundation.

## Configuration

Runtime configuration is managed by the `config` package.

- `config.settings.Settings` validates environment variables.
- `config.settings.get_settings()` loads settings from `.env` and environment variables.
- `config.logging.configure_logging()` configures human-readable process logging.

Required variables are documented in `.env.example`. Amazon-related variables are placeholders for future integration and should not contain real secrets in committed files.

## Setup

1. Create a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Fill in local values in `.env`.

Do not commit `.env` or any secret values.

## Amazon Ads Connection Test

After configuring Amazon Ads credentials in `.env`, run:

```powershell
python src/main.py
```

The connection test refreshes an OAuth access token and lists available advertising profiles. It does not download campaigns and does not include dashboard functionality.

## Amazon Ads Refresh Token Utility

After setting `AMAZON_ADS_CLIENT_ID`, `AMAZON_ADS_CLIENT_SECRET`, and `AMAZON_ADS_REDIRECT_URI` in `.env`, run:

```powershell
python src/generate_refresh_token.py
```

The utility displays a Login with Amazon authorization URL, asks for the returned authorization code, and prints only the refresh token. It does not save the token to `.env`.
