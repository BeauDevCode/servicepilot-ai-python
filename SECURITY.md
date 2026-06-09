# Security Policy

## Reporting

If you find a security issue, do not open a public issue with sensitive details.

Send a private report to the maintainer instead. Include:

- a short summary
- steps to reproduce
- affected files or routes
- suggested fix, if known

## Sensitive data

Do not commit:

- API keys
- `.env` files
- database files
- real customer records
- private logs
- screenshots with private information

## Project safety notes

- API keys are loaded from environment variables.
- The app works in mock mode without external API calls.
- Local SQLite files should stay out of git.
- Demo data should be fake or sanitized.
- Pull requests should not include secrets or private user data.

## Supported scope

This is a portfolio MVP. Security reports should focus on the public repository, local development setup, configuration, and demo behavior.
