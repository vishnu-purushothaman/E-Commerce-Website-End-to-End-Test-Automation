"""User registration, login, and logout journeys."""

import pytest
from playwright.sync_api import Page, expect

from automation.accounts import AccountFactory
from automation.config import settings
from automation.data import TestUser
from pages.auth_page import AuthPage
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
def test_home_page_loads_successfully(page: Page) -> None:
    home = HomePage(page)
    home.open_home()

    expect(page).to_have_title("Automation Exercise")
    expect(home.home_heading).to_be_visible()


@pytest.mark.ui
def test_register_user_and_verify_account_creation(
    page: Page,
    test_user: TestUser,
    account_factory: AccountFactory,
) -> None:
    home = HomePage(page)
    auth = AuthPage(page)
    home.open_home()
    home.open_signup_login()
    expect(auth.signup_heading).to_be_visible()

    auth.signup(test_user)
    expect(page.get_by_role("heading", name="Enter Account Information", exact=True)).to_be_visible()
    auth.complete_registration(test_user)
    account_factory.track(test_user)

    expect(page.get_by_text("ACCOUNT CREATED!", exact=True)).to_be_visible()
    page.get_by_role("link", name="Continue").click()
    expect(home.logged_in_as(test_user.name)).to_be_visible()

    home.delete_account()
    expect(page.get_by_text("ACCOUNT DELETED!", exact=True)).to_be_visible()
    account_factory.forget(test_user)


@pytest.mark.ui
def test_login_with_valid_credentials(
    page: Page,
    account_factory: AccountFactory,
) -> None:
    user = account_factory.create()
    home = HomePage(page)
    auth = AuthPage(page)
    home.open_home()
    home.open_signup_login()
    expect(auth.login_heading).to_be_visible()

    auth.login(user)

    expect(home.logged_in_as(user.name)).to_be_visible()


@pytest.mark.ui
def test_login_with_invalid_credentials_shows_error(page: Page, test_user: TestUser) -> None:
    home = HomePage(page)
    auth = AuthPage(page)
    home.open_home()
    home.open_signup_login()

    auth.login(test_user)

    expect(auth.login_error).to_be_visible()


@pytest.mark.ui
def test_logout_returns_user_to_login_page(
    page: Page,
    account_factory: AccountFactory,
) -> None:
    user = account_factory.create()
    home = HomePage(page)
    auth = AuthPage(page)
    home.open_home()
    home.open_signup_login()
    auth.login(user)
    expect(home.logged_in_as(user.name)).to_be_visible()

    home.logout()

    expect(page).to_have_url(f"{settings.base_url}/login")
    expect(auth.login_heading).to_be_visible()
