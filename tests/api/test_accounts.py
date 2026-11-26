"""Account lifecycle and login API checks."""

import pytest
from playwright.sync_api import APIRequestContext, APIResponse

from automation.accounts import AccountFactory


def api_payload(response: APIResponse, expected_code: int) -> dict:
    assert response.status == 200, f"Unexpected HTTP status: {response.status}"
    payload = response.json()
    assert payload.get("responseCode") == expected_code, payload
    return payload


@pytest.mark.api
def test_verify_login_accepts_valid_credentials(
    account_factory: AccountFactory,
    api_request: APIRequestContext,
) -> None:
    user = account_factory.create()
    payload = api_payload(
        api_request.post(
            "/api/verifyLogin",
            form={"email": user.email, "password": user.password},
        ),
        200,
    )

    assert payload["message"] == "User exists!"


@pytest.mark.api
def test_verify_login_rejects_invalid_credentials(api_request: APIRequestContext) -> None:
    payload = api_payload(
        api_request.post(
            "/api/verifyLogin",
            form={"email": "missing-user@example.test", "password": "invalid-password"},
        ),
        404,
    )

    assert payload["message"] == "User not found!"


@pytest.mark.api
@pytest.mark.parametrize(
    "form",
    [
        {"password": "test-password"},
        {"email": "qa@example.test"},
    ],
    ids=["missing-email", "missing-password"],
)
def test_verify_login_requires_email_and_password(
    api_request: APIRequestContext,
    form: dict[str, str],
) -> None:
    payload = api_payload(api_request.post("/api/verifyLogin", form=form), 400)

    assert payload["message"] == "Bad request, email or password parameter is missing in POST request."


@pytest.mark.api
def test_delete_method_on_verify_login_is_unsupported(api_request: APIRequestContext) -> None:
    payload = api_payload(
        api_request.delete("/api/verifyLogin", form={"email": "qa@example.test"}),
        405,
    )

    assert payload["message"] == "This request method is not supported."


@pytest.mark.api
def test_create_update_and_get_account(
    api_request: APIRequestContext,
    account_factory: AccountFactory,
) -> None:
    user = account_factory.create()

    updated_fields = user.account_payload()
    updated_fields["name"] = f"{user.name} Updated"
    updated = api_payload(api_request.put("/api/updateAccount", form=updated_fields), 200)
    assert updated["message"] == "User updated!"

    details = api_payload(
        api_request.get("/api/getUserDetailByEmail", params={"email": user.email}),
        200,
    )
    assert details["user"]["email"] == user.email
    assert details["user"]["name"] == updated_fields["name"]


@pytest.mark.api
def test_delete_account_removes_created_account(
    api_request: APIRequestContext,
    account_factory: AccountFactory,
) -> None:
    user = account_factory.create()
    deleted = api_payload(
        api_request.delete(
            "/api/deleteAccount",
            form={"email": user.email, "password": user.password},
        ),
        200,
    )
    account_factory.forget(user)
    assert deleted["message"] == "Account deleted!"

    login = api_payload(
        api_request.post(
            "/api/verifyLogin",
            form={"email": user.email, "password": user.password},
        ),
        404,
    )
    assert login["message"] == "User not found!"
