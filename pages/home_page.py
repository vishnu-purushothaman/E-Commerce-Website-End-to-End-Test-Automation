"""Home page and shared navigation actions."""

from playwright.sync_api import Locator

from pages.base_page import BasePage


class HomePage(BasePage):
    @property
    def home_heading(self) -> Locator:
        return self.page.get_by_role("heading", name="Full-Fledged practice website for Automation Engineers")

    def open_home(self) -> None:
        self.open_path("/")

    def open_signup_login(self) -> None:
        self.navigate("Signup / Login")

    def open_products(self) -> None:
        self.navigate("Products")

    def open_cart(self) -> None:
        self.navigate("Cart")

    def logged_in_as(self, name: str) -> Locator:
        return self.page.get_by_text(f"Logged in as {name}", exact=False)

    def logout(self) -> None:
        self.navigate("Logout")

    def delete_account(self) -> None:
        self.navigate("Delete Account")

    def subscribe(self, email: str) -> Locator:
        footer = self.page.locator("#footer")
        footer.scroll_into_view_if_needed()
        self.page.locator("#susbscribe_email").fill(email)
        self.page.locator("#subscribe").click()
        return self.page.locator("#success-subscribe")
