"""Shopping cart page actions."""

from playwright.sync_api import Locator

from pages.base_page import BasePage


class CartPage(BasePage):
    @property
    def rows(self) -> Locator:
        return self.page.locator("#cart_info_table tbody tr[id^='product-']")

    def row(self, index: int = 0) -> Locator:
        return self.rows.nth(index)

    def quantity(self, index: int = 0) -> Locator:
        return self.row(index).locator(".cart_quantity")

    def remove(self, index: int = 0) -> None:
        self.row(index).locator(".cart_quantity_delete").click()
