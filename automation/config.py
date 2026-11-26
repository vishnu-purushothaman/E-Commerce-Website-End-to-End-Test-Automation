"""Central settings for the Automation Exercise test suite."""

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("ECOMMERCE_BASE_URL", "https://automationexercise.com").rstrip("/")
    timeout_ms: int = int(os.getenv("PLAYWRIGHT_TIMEOUT_MS", "10000"))
    screenshot_dir: Path = PROJECT_ROOT / "artifacts" / "screenshots"


settings = Settings()
