from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from app.domain.exceptions.invalid_status_transition_error import (
    InvalidStatusTransitionError,
)
from app.domain.model.payee_status import PayeeStatus


@dataclass
class Payee:
    id: UUID
    name: str
    email: str
    bank_account: str
    status: PayeeStatus
    psp_reference: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        bank_account: str,
    ) -> "Payee":
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            name=name,
            email=email,
            bank_account=bank_account,
            status=PayeeStatus.PENDING,
            psp_reference=None,
            created_at=now,
            updated_at=now,
        )
    
    def set_psp_reference(self, psp_reference: str) -> None:
        self.psp_reference = psp_reference
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        self._transition_to(PayeeStatus.ACTIVE)
    
    def suspend(self) -> None:
        self._transition_to(PayeeStatus.SUSPENDED)
    
    def deactivate(self) -> None:
        self._transition_to(PayeeStatus.INACTIVE)
    
    def transition_to_status(self, new_status: PayeeStatus) -> None:
        self._transition_to(new_status)
    
    def _transition_to(self, new_status: PayeeStatus) -> None:
        if not self.status.can_transition_to(new_status):
            raise InvalidStatusTransitionError(
                f"Cannot transition from {self.status.value} to {new_status.value}"
            )
        self.status = new_status
        self.updated_at = datetime.utcnow()
    
    def mark_as_failed(self) -> None:
        self._transition_to(PayeeStatus.FAILED)
    
    @property
    def is_active(self) -> bool:
        return self.status == PayeeStatus.ACTIVE
    
    @property
    def can_receive_payments(self) -> bool:
        return self.status == PayeeStatus.ACTIVE and self.psp_reference is not None

