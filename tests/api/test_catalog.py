"""Catalog and search API checks."""

import pytest
from playwright.sync_api import APIRequestContext, APIResponse


def api_payload(response: APIResponse, expected_code: int) -> dict:
    assert response.status == 200, f"Unexpected HTTP status: {response.status}"
    payload = response.json()
    assert payload.get("responseCode") == expected_code, payload
    return payload


@pytest.mark.api
def test_get_all_products_returns_product_list(api_request: APIRequestContext) -> None:
    payload = api_payload(api_request.get("/api/productsList"), 200)

    assert payload["products"]
    assert {"id", "name", "price", "brand", "category"} <= payload["products"][0].keys()


@pytest.mark.api
def test_post_products_list_is_documented_as_unsupported(api_request: APIRequestContext) -> None:
    payload = api_payload(api_request.post("/api/productsList"), 405)

    assert payload["message"] == "This request method is not supported."


@pytest.mark.api
def test_get_all_brands_returns_brand_list(api_request: APIRequestContext) -> None:
    payload = api_payload(api_request.get("/api/brandsList"), 200)

    assert payload["brands"]
    assert {"id", "brand"} <= payload["brands"][0].keys()


@pytest.mark.api
def test_put_brands_list_is_documented_as_unsupported(api_request: APIRequestContext) -> None:
    payload = api_payload(api_request.put("/api/brandsList"), 405)

    assert payload["message"] == "This request method is not supported."


@pytest.mark.api
def test_search_products_returns_matching_results(api_request: APIRequestContext) -> None:
    payload = api_payload(
        api_request.post("/api/searchProduct", form={"search_product": "top"}),
        200,
    )

    assert payload["products"]
    assert all(
        "top" in product["name"].lower()
        or "top" in product["category"]["category"].lower()
        for product in payload["products"]
    )
    assert any("top" in product["name"].lower() for product in payload["products"])


@pytest.mark.api
def test_search_without_parameter_returns_documented_error(api_request: APIRequestContext) -> None:
    payload = api_payload(api_request.post("/api/searchProduct"), 400)

    assert payload["message"] == "Bad request, search_product parameter is missing in POST request."
