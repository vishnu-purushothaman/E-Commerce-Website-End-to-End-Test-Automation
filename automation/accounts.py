"""Create and clean up disposable accounts through the documented API."""

from playwright.sync_api import APIRequestContext

from automation.data import TestUser


class AccountFactory:
    def __init__(self, request: APIRequestContext) -> None:
        self._request = request
        self._accounts_to_clean: list[TestUser] = []

    def create(self) -> TestUser:
        user = TestUser.create()
        response = self._request.post("/api/createAccount", form=user.account_payload())
        assert response.status == 200, f"Unexpected HTTP status creating account: {response.status}"
        payload = response.json()
        if payload.get("responseCode") == 201:
            self.track(user)
        assert payload.get("responseCode") == 201, f"Account creation failed: {payload}"
        assert payload.get("message") == "User created!", f"Unexpected account creation response: {payload}"
        return user

    def track(self, user: TestUser) -> None:
        if user not in self._accounts_to_clean:
            self._accounts_to_clean.append(user)

    def forget(self, user: TestUser) -> None:
        if user in self._accounts_to_clean:
            self._accounts_to_clean.remove(user)

    def cleanup(self) -> None:
        def delete_account(user: TestUser) -> None:
            response = self._request.delete(
                "/api/deleteAccount",
                form={"email": user.email, "password": user.password},
            )
            assert response.status == 200, f"Unexpected HTTP status deleting account: {response.status}"
            payload = response.json()
            assert payload.get("responseCode") == 200, f"Account cleanup failed: {payload}"

        while self._accounts_to_clean:
            user = self._accounts_to_clean[-1]
            delete_account(user)
            self._accounts_to_clean.pop()
