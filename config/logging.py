"""Logging configuration for Filymore OS."""

import logging

from config.settings import Settings


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(settings: Settings) -> None:
    """Configure process-wide human-readable logging."""

    logging.basicConfig(
        level=settings.log_level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        force=True,
    )
