"""
Pytest configuration and shared fixtures for the test suite.
"""
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest


@pytest.fixture
def sample_payee_data():
    """Sample payee data for testing."""
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "bank_account": "GB29NWBK60161331926819",
    }

