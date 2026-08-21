from pathlib import PurePath

import pytest
from tests.pytest_contract import inferred_taxonomy_marker, resolved_taxonomy_marker


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("tests/unit/test_settings.py", "unit"),
        ("tests/api/test_health.py", "component"),
        ("tests/services/test_health_service.py", "component"),
        ("tests/integration/test_database.py", "integration"),
    ],
)
def test_inferred_taxonomy_marker(path: str, expected: str) -> None:
    assert inferred_taxonomy_marker(PurePath(path)) == expected


def test_resolved_taxonomy_marker_prefers_explicit_marker() -> None:
    assert resolved_taxonomy_marker({"unit"}, PurePath("tests/api/test_health.py")) == "unit"


def test_resolved_taxonomy_marker_rejects_multiple_explicit_markers() -> None:
    with pytest.raises(ValueError, match="multiple taxonomy markers"):
        resolved_taxonomy_marker({"unit", "component"}, PurePath("tests/test_example.py"))
