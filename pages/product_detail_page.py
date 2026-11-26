"""Product detail view actions."""

from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    def set_quantity(self, quantity: int) -> None:
        self.page.locator("#quantity").fill(str(quantity))

    def add_to_cart(self) -> None:
        self.page.get_by_role("button", name="Add to cart").click()

    def view_cart_from_modal(self) -> None:
        self.page.get_by_role("link", name="View Cart").click()
