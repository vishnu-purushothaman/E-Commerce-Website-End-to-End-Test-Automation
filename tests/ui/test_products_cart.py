"""Product browsing and shopping cart journeys."""

import pytest
from playwright.sync_api import Page, expect

from automation.config import settings
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage
from pages.products_page import ProductsPage


@pytest.mark.ui
def test_navigate_to_products_page(page: Page) -> None:
    home = HomePage(page)
    home.open_home()
    home.open_products()

    expect(page).to_have_url(f"{settings.base_url}/products")
    expect(ProductsPage(page).products_heading).to_be_visible()
    expect(ProductsPage(page).product_cards.first).to_be_visible()


@pytest.mark.ui
def test_search_product_and_verify_results(page: Page) -> None:
    products = ProductsPage(page)
    products.open()
    products.search("top")

    expect(products.searched_heading).to_be_visible()
    expect(products.product_cards.first).to_be_visible()
    expect(products.product_cards.first).to_contain_text("Top")


@pytest.mark.ui
def test_view_product_details(page: Page) -> None:
    products = ProductsPage(page)
    products.open()
    products.view_product()

    for label in ("Category:", "Rs.", "Availability:", "Condition:", "Brand:"):
        expect(page.get_by_text(label, exact=False).first).to_be_visible()
    expect(page.locator(".product-information h2")).to_be_visible()


@pytest.mark.ui
def test_add_product_and_verify_cart_details(page: Page) -> None:
    products = ProductsPage(page)
    products.open()
    products.add_product_to_cart()
    products.view_cart_from_modal()

    cart = CartPage(page)
    expect(cart.rows).to_have_count(1)
    expect(cart.quantity()).to_have_text("1")
    expect(cart.row().locator(".cart_price")).to_be_visible()
    expect(cart.row().locator(".cart_total")).to_be_visible()


@pytest.mark.ui
def test_product_quantity_is_preserved_in_cart(page: Page) -> None:
    products = ProductsPage(page)
    products.open()
    products.view_product()
    detail = ProductDetailPage(page)
    expect(page.locator(".product-information h2")).to_be_visible()
    detail.set_quantity(4)
    detail.add_to_cart()
    detail.view_cart_from_modal()

    expect(CartPage(page).quantity()).to_have_text("4")


@pytest.mark.ui
def test_remove_product_from_cart(page: Page) -> None:
    products = ProductsPage(page)
    products.open()
    products.add_product_to_cart()
    products.view_cart_from_modal()
    cart = CartPage(page)
    expect(cart.rows).to_have_count(1)

    cart.remove()

    expect(cart.rows).to_have_count(0)
    expect(page.get_by_text("Cart is empty!", exact=False)).to_be_visible()
