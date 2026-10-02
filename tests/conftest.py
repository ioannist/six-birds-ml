from __future__ import annotations

import pytest


def pytest_configure(config) -> None:
    config.addinivalue_line("markers", "slow: extended extended checks")
    config.addinivalue_line("markers", "release: full release audit regeneration")


def pytest_collection_modifyitems(config, items) -> None:
    markexpr = config.option.markexpr or ""
    run_slow = "slow" in markexpr
    run_release = "release" in markexpr
    skip_slow = pytest.mark.skip(reason="slow test; run with pytest -m slow")
    skip_release = pytest.mark.skip(
        reason="release test; run with pytest -m release"
    )
    for item in items:
        if "release" in item.keywords and not run_release:
            item.add_marker(skip_release)
        elif "slow" in item.keywords and not run_slow:
            item.add_marker(skip_slow)
