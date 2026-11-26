"""Shared page behavior."""

from playwright.sync_api import Page

from automation.config import settings


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(settings.timeout_ms)

    def open_path(self, path: str = "/") -> None:
        self.page.goto(f"{settings.base_url}{path}", wait_until="domcontentloaded")

    def navigate(self, name: str) -> None:
        self.page.get_by_role("link", name=name).click()
