"""
Unit tests for the Payee domain entity.
"""
import pytest

from app.domain.model import Payee, PayeeStatus


class TestPayeeCreation:
    """Test cases for creating a Payee."""

    def test_create_payee_with_valid_data(self, sample_payee_data):
        """Test creating a payee with valid data."""
        payee = Payee.create(
            name=sample_payee_data["name"],
            email=sample_payee_data["email"],
            bank_account=sample_payee_data["bank_account"],
        )

        assert payee.id is not None
        assert payee.name == sample_payee_data["name"]
        assert payee.email == sample_payee_data["email"]
        assert payee.bank_account == sample_payee_data["bank_account"]
        assert payee.status == PayeeStatus.PENDING
        assert payee.psp_reference is None
        assert payee.created_at is not None
        assert payee.updated_at is not None


class TestPayeeStatusTransitions:
    """Test cases for payee status transitions."""

    def test_activate_payee(self, sample_payee_data):
        """Test activating a payee."""
        payee = Payee.create(**sample_payee_data)
        payee.activate()
        
        assert payee.status == PayeeStatus.ONBOARDED

    def test_mark_payee_as_failed(self, sample_payee_data):
        """Test marking a payee as failed."""
        payee = Payee.create(**sample_payee_data)
        payee.mark_as_failed()
        
        assert payee.status == PayeeStatus.FAILED

    def test_set_psp_reference(self, sample_payee_data):
        """Test setting PSP reference."""
        payee = Payee.create(**sample_payee_data)
        psp_ref = "PSP-REF-12345"
        payee.set_psp_reference(psp_ref)
        
        assert payee.psp_reference == psp_ref

