"""Application settings loaded from environment variables."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from amazon.ads.constants import (
    AMAZON_ADS_DEFAULT_API_BASE_URL,
    AMAZON_ADS_DEFAULT_TOKEN_URL,
)


Environment = Literal["development", "staging", "production", "test"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """Validated runtime configuration for Filymore OS."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    environment: Environment = Field(alias="ENVIRONMENT")
    debug: bool = Field(alias="DEBUG")

    app_name: str = Field(alias="APP_NAME", min_length=1)
    app_host: str = Field(alias="APP_HOST", min_length=1)
    app_port: int = Field(alias="APP_PORT", ge=1, le=65535)

    log_level: LogLevel = Field(alias="LOG_LEVEL")

    database_url: str | None = Field(default=None, alias="DATABASE_URL")

    amazon_ads_client_id: str | None = Field(default=None, alias="AMAZON_ADS_CLIENT_ID")
    amazon_ads_client_secret: SecretStr | None = Field(
        default=None,
        alias="AMAZON_ADS_CLIENT_SECRET",
    )
    amazon_ads_refresh_token: SecretStr | None = Field(
        default=None,
        alias="AMAZON_ADS_REFRESH_TOKEN",
    )
    amazon_ads_redirect_uri: str | None = Field(default=None, alias="AMAZON_ADS_REDIRECT_URI")
    amazon_ads_profile_id: str | None = Field(default=None, alias="AMAZON_ADS_PROFILE_ID")
    amazon_ads_api_base_url: str = Field(
        default=AMAZON_ADS_DEFAULT_API_BASE_URL,
        alias="AMAZON_ADS_API_BASE_URL",
    )
    amazon_ads_token_url: str = Field(
        default=AMAZON_ADS_DEFAULT_TOKEN_URL,
        alias="AMAZON_ADS_TOKEN_URL",
    )
    amazon_ads_request_timeout_seconds: float = Field(
        default=30.0,
        alias="AMAZON_ADS_REQUEST_TIMEOUT_SECONDS",
        gt=0,
    )

    sp_api_client_id: str | None = Field(default=None, alias="SP_API_CLIENT_ID")
    sp_api_client_secret: SecretStr | None = Field(
        default=None,
        alias="SP_API_CLIENT_SECRET",
    )
    sp_api_refresh_token: SecretStr | None = Field(
        default=None,
        alias="SP_API_REFRESH_TOKEN",
    )

    aws_access_key_id: str | None = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: SecretStr | None = Field(
        default=None,
        alias="AWS_SECRET_ACCESS_KEY",
    )
    aws_region: str | None = Field(default=None, alias="AWS_REGION")
    aws_role_arn: str | None = Field(default=None, alias="AWS_ROLE_ARN")


@lru_cache
def get_settings() -> Settings:
    """Return cached validated settings."""

    return Settings()
