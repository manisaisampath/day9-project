
# Project Instructions

## Project Overview
This is a reusable Python project skeleton for AI applications.

## Python Environment
- Use Python 3.12 or higher.
- Use uv for dependency management.
- Do not use global Python packages.

## Project Structure
- Application source code must be inside src/day_9_project/.
- Automated tests must be inside tests/.

## Coding Standards
- Use type hints for functions.
- Follow PEP 8 coding conventions.
- Use Ruff for linting and formatting.
- Use Pydantic for data validation.
- Use HTTPX for asynchronous HTTP requests.

## Testing
- Use pytest for automated tests.
- Write tests for successful responses, errors, retries and timeouts.
- Use mock responses instead of real external API calls.
- Run tests before committing changes.

## Security
- Store secrets in environment variables.
- Never hardcode API keys or passwords.
- Never commit .env files.
