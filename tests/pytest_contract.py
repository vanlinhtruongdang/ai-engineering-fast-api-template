"""Pytest taxonomy rules shared by every local test command."""

from collections.abc import Collection
from pathlib import PurePath

import pytest

TAXONOMY_MARKERS = frozenset({"unit", "component", "integration", "acceptance", "live"})
_COMPONENT_DIRECTORIES = frozenset({"api", "services", "cli", "pipelines", "agents"})


def inferred_taxonomy_marker(path: PurePath) -> str:
    """Return the default taxonomy marker for a test module path."""

    parts = path.parts
    try:
        test_area = parts[parts.index("tests") + 1]
    except (ValueError, IndexError):
        return "unit"

    if test_area == "integration":
        return "integration"
    if test_area in _COMPONENT_DIRECTORIES:
        return "component"
    return "unit"


def resolved_taxonomy_marker(marker_names: Collection[str], path: PurePath) -> str:
    """Return the explicit marker or infer one, rejecting ambiguity."""

    explicit_markers = TAXONOMY_MARKERS.intersection(marker_names)
    if len(explicit_markers) > 1:
        markers = ", ".join(sorted(explicit_markers))
        raise ValueError(f"test has multiple taxonomy markers: {markers}")
    if explicit_markers:
        return next(iter(explicit_markers))
    return inferred_taxonomy_marker(path)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Ensure every collected test belongs to one primary taxonomy lane."""

    for item in items:
        marker_names = {marker.name for marker in item.iter_markers()}
        try:
            taxonomy_marker = resolved_taxonomy_marker(marker_names, item.path)
        except ValueError as error:
            raise pytest.UsageError(f"{item.nodeid}: {error}") from error
        if taxonomy_marker not in marker_names:
            item.add_marker(getattr(pytest.mark, taxonomy_marker))
