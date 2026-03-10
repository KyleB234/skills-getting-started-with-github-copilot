import copy

import pytest

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory `activities` dict before each test."""
    original = copy.deepcopy(app_module.activities)
    yield
    # Preserve the same dict object so any references remain valid.
    app_module.activities.clear()
    app_module.activities.update(original)
