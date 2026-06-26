# Configuration

Filymore OS uses a dedicated `config` package for runtime settings and logging setup.

## Environment Loading

Settings are loaded by `config.settings.Settings` using `pydantic-settings`.

Values are read from:

1. Operating system environment variables.
2. A local `.env` file.

Committed defaults and examples live in `.env.example`. Local `.env` files are ignored by Git.

## Required Variables

The following variables are required:

```text
ENVIRONMENT
DEBUG
APP_NAME
APP_HOST
APP_PORT
LOG_LEVEL
```

`DATABASE_URL` is optional until the database foundation is implemented.

## Amazon Ads Configuration

The following Amazon Ads variables are used by the Amazon Ads authentication module:

```text
AMAZON_ADS_CLIENT_ID
AMAZON_ADS_CLIENT_SECRET
AMAZON_ADS_REFRESH_TOKEN
AMAZON_ADS_REDIRECT_URI
AMAZON_ADS_PROFILE_ID
AMAZON_ADS_API_BASE_URL
AMAZON_ADS_TOKEN_URL
AMAZON_ADS_REQUEST_TIMEOUT_SECONDS
```

`AMAZON_ADS_CLIENT_SECRET` and `AMAZON_ADS_REFRESH_TOKEN` are secret values and must never be committed or logged.

## Amazon SP-API and AWS Placeholders

The following variables are included as placeholders only:

```text
SP_API_CLIENT_ID
SP_API_CLIENT_SECRET
SP_API_REFRESH_TOKEN
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
AWS_ROLE_ARN
```

Filymore OS does not connect to Amazon SP-API or AWS in this milestone.

## Secret Handling

Never commit real secrets.

Secret values are represented with Pydantic secret types where applicable. Do not log settings objects directly, and do not print environment values that may contain credentials or tokens.

## Logging

Logging is configured through `config.logging.configure_logging`.

The current format is human-readable:

```text
YYYY-MM-DD HH:MM:SS | LEVEL | logger.name | message
```

JSON logging can be introduced later when deployment and observability requirements are defined.
