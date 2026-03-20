# User Management API Challenge

This repository contains an end-to-end API test suite for the User Management API challenge.

## Tech Stack

- Python 3.12
- pytest
- requests
- pytest-html
- Docker
- GitHub Actions

## Project Structure

- `tests/` -> API test suite
- `docs/bugs.md` -> documented bugs found during testing
- `reports/` -> generated HTML test reports
- `.github/workflows/api-tests.yml` -> CI pipeline

## Prerequisites

- Python 3.12
- Docker installed and running

## Run the API locally

    docker run -p 3000:3000 ghcr.io/danielsilva-loanpro/sdet-interview-challenge:latest

The API will be available at:

    http://localhost:3000

## Install dependencies

    python -m venv .venv
    source .venv/Scripts/activate
    pip install -r requirements.txt

## Run tests

## Notes

Some tests are intentionally marked as `xfail` because they expose known discrepancies between the API behavior and the OpenAPI specification.

This was done to preserve the bug coverage while keeping the CI pipeline readable and maintainable.

Each `xfail` test includes a clear reason message describing the bug that was found. Full details are documented in:

    docs/bugs.md
    

Run the full suite:

    python -m pytest tests

Run only dev tests:

    python -m pytest tests --env dev

Run only prod tests:

    python -m pytest tests --env prod

Run only cross-environment tests:

    python -m pytest tests -m "cross_env"

## Generate HTML report

    python -m pytest tests --html=reports/report.html --self-contained-html

## Known Bugs

Documented discrepancies between the API behavior and the specification can be found in:

    docs/bugs.md

## CI Pipeline

The GitHub Actions workflow runs:

- environment-specific tests for `dev`
- environment-specific tests for `prod`
- cross-environment tests separately

Workflow file:

    .github/workflows/api-tests.yml
