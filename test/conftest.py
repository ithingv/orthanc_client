"""
Configuration for pytest

python 3.9.1
pytest 7.1.2
"""

import pytest

@pytest.fixture
def test_config():
    return "Testing Configuration"
