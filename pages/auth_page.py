"""Signup and login page actions."""

from playwright.sync_api import Locator

from automation.data import TestUser
from pages.base_page import BasePage


class AuthPage(BasePage):
    @property
    def login_heading(self) -> Locator:
        return self.page.get_by_role("heading", name="Login to your account")

    @property
    def signup_heading(self) -> Locator:
        return self.page.get_by_role("heading", name="New User Signup!")

    @property
    def login_error(self) -> Locator:
        return self.page.get_by_text("Your email or password is incorrect!", exact=True)

    @property
    def signup_error(self) -> Locator:
        return self.page.get_by_text("Email Address already exist!", exact=True)

    def signup(self, user: TestUser) -> None:
        self.page.locator("[data-qa='signup-name']").fill(user.name)
        self.page.locator("[data-qa='signup-email']").fill(user.email)
        self.page.locator("[data-qa='signup-button']").click()

    def complete_registration(self, user: TestUser) -> None:
        self.page.locator("#id_gender1").check()
        self.page.locator("#password").fill(user.password)
        self.page.locator("#days").select_option("15")
        self.page.locator("#months").select_option("6")
        self.page.locator("#years").select_option("1990")
        self.page.locator("#newsletter").check()
        self.page.locator("#optin").check()
        self.page.locator("#first_name").fill("QA")
        self.page.locator("#last_name").fill("Tester")
        self.page.locator("#company").fill("Example Test Company")
        self.page.locator("#address1").fill("1 Example Street")
        self.page.locator("#address2").fill("Suite 1")
        self.page.locator("#country").select_option(label="United States")
        self.page.locator("#state").fill("Test State")
        self.page.locator("#city").fill("Test City")
        self.page.locator("#zipcode").fill("00000")
        self.page.locator("#mobile_number").fill("0000000000")
        self.page.locator("[data-qa='create-account']").click()

    def login(self, user: TestUser) -> None:
        self.page.locator("[data-qa='login-email']").fill(user.email)
        self.page.locator("[data-qa='login-password']").fill(user.password)
        self.page.locator("[data-qa='login-button']").click()
