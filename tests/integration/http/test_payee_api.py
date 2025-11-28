"""
Integration tests for the Payee API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client():
    """Create a test client."""
    app = create_app()
    return TestClient(app)


class TestPayeeAPI:
    """Integration tests for payee endpoints."""

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "payee-onboarding"

    def test_onboard_payee_endpoint(self, client, sample_payee_data):
        """Test the onboard payee endpoint."""
        response = client.post("/api/payees", json=sample_payee_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["name"] == sample_payee_data["name"]
        assert data["email"] == sample_payee_data["email"]
        assert data["bank_account"] == sample_payee_data["bank_account"]
        assert data["status"] in ["PENDING", "ONBOARDED"]

    def test_onboard_payee_with_invalid_email(self, client, sample_payee_data):
        """Test onboarding with invalid email."""
        invalid_data = sample_payee_data.copy()
        invalid_data["email"] = "invalid-email"
        
        response = client.post("/api/payees", json=invalid_data)
        
        assert response.status_code == 422  # Validation error

