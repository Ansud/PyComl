from pathlib import Path
from typing import Any

import pytest


@pytest.fixture(autouse=True)
def app_settings(monkeypatch: Any, tmp_path: Path) -> None:
    monkeypatch.setattr("app.core.config.loader.Settings.SETTINGS_BASE_PATH", tmp_path)
