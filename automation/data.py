"""Synthetic, disposable test data."""

from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class TestUser:
    __test__ = False

    name: str
    email: str
    password: str

    @classmethod
    def create(cls) -> "TestUser":
        unique_id = uuid4().hex
        return cls(
            name=f"QA Tester {unique_id[:8]}",
            email=f"qa-{unique_id}@example.test",
            password=f"TestOnly-{uuid4().hex[:16]}!",
        )

    def account_payload(self) -> dict[str, str]:
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "title": "Mr",
            "birth_date": "15",
            "birth_month": "6",
            "birth_year": "1990",
            "firstname": "QA",
            "lastname": "Tester",
            "company": "Example Test Company",
            "address1": "1 Example Street",
            "address2": "",
            "country": "United States",
            "zipcode": "00000",
            "state": "Test State",
            "city": "Test City",
            "mobile_number": "0000000000",
        }
