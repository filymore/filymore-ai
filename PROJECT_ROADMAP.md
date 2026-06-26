# Filymore OS Project Roadmap

## Project Vision

Filymore OS is planned as a production-grade operating layer for managing business workflows, integrations, data, and operational visibility in a clean Python-based system.

## Business Goals

- Establish a reliable technical foundation for future product development.
- Support secure integrations with Amazon advertising and marketplace services.
- Provide clear operational visibility through configuration, logging, data storage, and documentation standards.
- Build incrementally with maintainable architecture and traceable milestones.

## Current Milestone

FOS-003: Amazon Advertising API Authentication

The current milestone establishes Amazon Advertising OAuth authentication and a profile-listing connection test. Dashboard features and campaign downloads are intentionally excluded.

## Completed Features

- FOS-001: Initial project scaffold
- Local Git repository initialized
- Enterprise folder structure created
- FOS-002: Configuration and logging foundation
- Amazon Ads OAuth authentication module
- Amazon Ads advertising profile connection test
- Amazon Ads one-time refresh token generation utility

## Upcoming Features

- Configuration validation tests
- Application entrypoint
- Database foundation
- Amazon Ads campaign download workflows
- Amazon SP-API integration
- Dashboard foundation
- Data ingestion and processing workflows

## Architecture Decisions

- Use a Python `src` layout for application source code.
- Keep configuration isolated in the `config` package.
- Load local environment values from `.env`.
- Validate settings with typed Pydantic models.
- Treat secrets as sensitive values and never print them.
- Use human-readable structured logging before introducing JSON logging.
- Keep Amazon OAuth authentication separate from API calls.
- Inject authenticated HTTP clients into Amazon API clients.
- Keep Amazon API URLs and integration constants in `amazon/ads/constants.py`.

## Version History

| Version | Milestone | Description |
| --- | --- | --- |
| 0.1.0 | FOS-001 | Initial project scaffold |
| 0.2.0 | FOS-002 | Configuration and logging foundation |
| 0.3.0 | FOS-003 | Amazon Advertising API authentication and profile connection test |
| 0.3.1 | FOS-003B | Amazon Advertising API refresh token generator |
