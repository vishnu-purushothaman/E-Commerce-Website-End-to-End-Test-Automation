"""Category, brand, and subscription checks."""

import pytest
from playwright.sync_api import Page, expect

from automation.config import settings
from automation.data import TestUser
from pages.home_page import HomePage
from pages.products_page import ProductsPage


@pytest.mark.ui
def test_navigate_through_product_categories(page: Page) -> None:
    home = HomePage(page)
    home.open_home()
    products = ProductsPage(page)
    products.open_category("Women")
    products.open_category("Tops")

    expect(page).to_have_url(f"{settings.base_url}/category_products/2")
    expect(page.get_by_role("heading", name="Women - Tops Products", exact=False)).to_be_visible()

    products.open_category("Men")
    products.open_category("Jeans")
    expect(page).to_have_url(f"{settings.base_url}/category_products/6")
    expect(page.get_by_role("heading", name="Men - Jeans Products", exact=False)).to_be_visible()


@pytest.mark.ui
def test_navigate_through_product_brands(page: Page) -> None:
    products = ProductsPage(page)
    products.open()
    products.open_brand("Polo")

    expect(page).to_have_url(f"{settings.base_url}/brand_products/Polo")
    expect(page.get_by_role("heading", name="Brand - Polo Products", exact=False)).to_be_visible()

    products.open_brand("H&M")
    expect(page).to_have_url(f"{settings.base_url}/brand_products/H&M")
    expect(page.get_by_role("heading", name="Brand - H&M Products", exact=False)).to_be_visible()


@pytest.mark.ui
def test_subscription_succeeds_on_home_page(
    page: Page,
    test_user: TestUser,
) -> None:
    home = HomePage(page)
    home.open_home()

    success = home.subscribe(test_user.email)

    expect(success).to_contain_text("You have been successfully subscribed!")
