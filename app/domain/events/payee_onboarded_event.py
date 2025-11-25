from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.events.domain_event import DomainEvent


@dataclass
class PayeeOnboardedEvent(DomainEvent):
    event_type: str
    payee_id: UUID
    name: str
    email: str
    psp_reference: str
    timestamp: datetime

    @classmethod
    def create(
        cls,
        payee_id: UUID,
        name: str,
        email: str,
        psp_reference: str,
        timestamp: datetime,
    ) -> "PayeeOnboardedEvent":
        return cls(
            event_type="payee_onboarded",
            payee_id=payee_id,
            name=name,
            email=email,
            psp_reference=psp_reference,
            timestamp=timestamp,
        )

