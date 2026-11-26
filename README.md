# E-Commerce Website End-to-End Test Automation

A learning-oriented Python framework for UI and REST API testing of the public
[Automation Exercise](https://automationexercise.com/) practice site. It uses
Playwright, Pytest, the Page Object Model, and Pytest-HTML.

The site is shared and may change or be temporarily unavailable. Tests report
the behavior actually observed; they do not place orders or submit payment
details. Account tests use unique, synthetic `example.test` addresses and
remove accounts they create.

## Project layout

```text
automation/       Shared settings, synthetic test data, and account cleanup
pages/            UI Page Object Model
tests/api/        Catalog, search, authentication, and account API tests
tests/ui/         Registration, login, products, cart, navigation, subscription
.github/workflows GitHub Actions workflow and report artifact upload
```

## Requirements

- Python 3.10 or later
- Google Chrome/Chromium browser dependencies (installed by Playwright)
- Network access to `https://automationexercise.com`

## Install

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
```

If a corporate Windows certificate proxy prevents Playwright from downloading
Chromium, enable the Node driver's Windows certificate store for that install:

```powershell
$env:NODE_USE_SYSTEM_CA = "1"
python -m playwright install chromium
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run tests

Run all UI and API tests:

```bash
pytest
```

Run one suite or select markers:

```bash
pytest tests/ui
pytest tests/api
pytest -m smoke
```

The suite launches Chromium headlessly by default through pytest-playwright.
Open `report.html` after a run for the self-contained HTML report. Screenshots
for failed UI calls are written to `artifacts/screenshots/`.

Optional environment settings:

- `ECOMMERCE_BASE_URL`: target base URL (defaults to the official site).
- `PLAYWRIGHT_TIMEOUT_MS`: per-action browser timeout in milliseconds (default
  `10000`).

## Test coverage

The UI suite covers home-page loading, signup and account creation, valid and
invalid login, logout, product navigation/search/details, cart add/quantity/
remove, category and brand navigation, and subscription. Scenarios follow the
official [UI test cases](https://automationexercise.com/test_cases).

The API suite covers product and brand lists, product search, valid and invalid
login, missing login/search parameters, documented unsupported methods, and
the create/update/read/delete account lifecycle.

## Continuous integration

GitHub Actions runs `pytest` on pushes, pull requests, and manual dispatch. The
workflow installs Chromium, generates `report.html`, and uploads the report and
failure screenshots as the `automation-test-results` artifact, including when
tests fail.

## Learning path

1. Start with `tests/ui/test_auth.py` and trace each action into its page object.
2. Read `tests/conftest.py` to see shared fixtures and failure screenshots.
3. Compare API tests with the official [API scenarios](https://automationexercise.com/api_list).
4. Run an individual test, inspect the HTML report, and extend one scenario at a
   time.
