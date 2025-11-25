from enum import Enum


class PayeeStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    INACTIVE = "INACTIVE"
    FAILED = "FAILED"
    
    def can_transition_to(self, new_status: "PayeeStatus") -> bool:
        allowed_transitions = {
            PayeeStatus.PENDING: [
                PayeeStatus.ACTIVE,
                PayeeStatus.INACTIVE,
                PayeeStatus.FAILED,
            ],
            PayeeStatus.ACTIVE: [PayeeStatus.SUSPENDED, PayeeStatus.INACTIVE],
            PayeeStatus.SUSPENDED: [
                PayeeStatus.ACTIVE,
                PayeeStatus.INACTIVE,
            ],
            PayeeStatus.INACTIVE: [],
            PayeeStatus.FAILED: [
                PayeeStatus.PENDING,
                PayeeStatus.INACTIVE,
            ],
        }
        return new_status in allowed_transitions.get(self, [])

