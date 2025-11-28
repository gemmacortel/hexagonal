"""
Unit tests for the OnboardPayeeService application service.
"""
from unittest.mock import Mock, MagicMock
from uuid import uuid4

import pytest

from app.application.dtos import OnboardPayeeRequest
from app.application.onboard_payee import OnboardPayeeService
from app.domain.model import Payee


class TestOnboardPayeeService:
    """Test cases for the OnboardPayeeService."""

    @pytest.fixture
    def mock_repository(self):
        """Mock repository."""
        return Mock()

    @pytest.fixture
    def mock_psp_client(self):
        """Mock PSP client."""
        client = Mock()
        client.onboard_payee.return_value = "PSP-REF-12345"
        return client

    @pytest.fixture
    def mock_event_publisher(self):
        """Mock event publisher."""
        return Mock()

    @pytest.fixture
    def service(self, mock_repository, mock_psp_client, mock_event_publisher):
        """Create service with mocked dependencies."""
        return OnboardPayeeService(
            repository=mock_repository,
            psp_client=mock_psp_client,
            publish_payee_onboarded_event=mock_event_publisher,
        )

    def test_successful_payee_onboarding(
        self, service, mock_repository, mock_psp_client, mock_event_publisher, sample_payee_data
    ):
        """Test successful payee onboarding flow."""
        request = OnboardPayeeRequest(**sample_payee_data)
        
        response = service.execute(request)

        # Verify repository interactions
        assert mock_repository.save.called
        assert mock_repository.update.called

        # Verify PSP client was called
        mock_psp_client.onboard_payee.assert_called_once()

        # Verify event was published
        assert mock_event_publisher.execute.called

        # Verify response
        assert response.name == sample_payee_data["name"]
        assert response.email == sample_payee_data["email"]
        assert response.psp_reference == "PSP-REF-12345"
        assert response.status == "ONBOARDED"

    def test_payee_onboarding_failure(
        self, service, mock_repository, mock_psp_client, mock_event_publisher, sample_payee_data
    ):
        """Test payee onboarding when PSP fails."""
        request = OnboardPayeeRequest(**sample_payee_data)
        mock_psp_client.onboard_payee.side_effect = Exception("PSP Error")

        with pytest.raises(Exception, match="PSP Error"):
            service.execute(request)

        # Verify payee was marked as failed
        mock_repository.update.assert_called_once()
        saved_payee = mock_repository.update.call_args[0][0]
        assert saved_payee.status.value == "FAILED"

