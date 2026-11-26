"""Product listing, search, category, and brand interactions."""

from playwright.sync_api import Locator

from pages.base_page import BasePage


class ProductsPage(BasePage):
    @property
    def product_cards(self) -> Locator:
        return self.page.locator(".features_items .product-image-wrapper")

    @property
    def products_heading(self) -> Locator:
        return self.page.get_by_role("heading", name="All Products", exact=True)

    @property
    def searched_heading(self) -> Locator:
        return self.page.get_by_role("heading", name="Searched Products", exact=True)

    def open(self) -> None:
        self.open_path("/products")

    def search(self, term: str) -> None:
        self.page.locator("#search_product").fill(term)
        self.page.locator("#submit_search").click()

    def view_product(self, index: int = 0) -> None:
        self.product_cards.nth(index).get_by_role("link", name="View Product").click()

    def add_product_to_cart(self, index: int = 0) -> None:
        card = self.product_cards.nth(index)
        card.hover()
        card.locator(".product-overlay .add-to-cart").click()

    def continue_shopping(self) -> None:
        self.page.get_by_role("button", name="Continue Shopping").click()

    def view_cart_from_modal(self) -> None:
        self.page.get_by_role("link", name="View Cart").click()

    def open_category(self, category: str) -> None:
        self.page.locator("#accordian").get_by_role("link", name=category, exact=False).click()

    def open_brand(self, brand: str) -> None:
        self.page.locator("#brands_products").get_by_role("link", name=brand, exact=False).click()
