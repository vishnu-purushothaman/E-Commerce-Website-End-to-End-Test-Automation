"""Shared pytest fixtures and failure screenshots."""

from collections.abc import Iterator
import os
import re
from datetime import datetime, timezone

if os.name == "nt":
    os.environ.setdefault("NODE_USE_SYSTEM_CA", "1")

import pytest
from playwright.sync_api import APIRequestContext, Error, Page, Playwright

from automation.accounts import AccountFactory
from automation.config import settings
from automation.data import TestUser


@pytest.fixture(scope="session")
def api_request(playwright: Playwright) -> Iterator[APIRequestContext]:
    request = playwright.request.new_context(
        base_url=settings.base_url,
        extra_http_headers={"Accept": "application/json"},
    )
    yield request
    request.dispose()


@pytest.fixture
def account_factory(api_request: APIRequestContext) -> Iterator[AccountFactory]:
    factory = AccountFactory(api_request)
    yield factory
    factory.cleanup()


@pytest.fixture
def test_user() -> TestUser:
    return TestUser.create()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]) -> Iterator[None]:
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if not isinstance(page, Page) or page.is_closed():
        return

    settings.screenshot_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.nodeid)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    screenshot = settings.screenshot_dir / f"{safe_name}_{timestamp}.png"
    try:
        page.screenshot(path=str(screenshot), full_page=True)
        report.sections.append(("Failure screenshot", str(screenshot)))
    except Error as error:
        report.sections.append(("Failure screenshot", f"Could not capture screenshot: {error}"))
