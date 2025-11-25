from typing import Dict, Optional
from uuid import UUID

from app.domain.model import Payee
from app.domain.ports import PayeeRepository


class InMemoryPayeeRepository(PayeeRepository):
    def __init__(self):
        self._storage: Dict[UUID, Payee] = {}
    
    def save(self, payee: Payee) -> None:
        self._storage[payee.id] = payee
    
    def find_by_id(self, payee_id: UUID) -> Optional[Payee]:
        return self._storage.get(payee_id)
    
    def update(self, payee: Payee) -> None:
        if payee.id not in self._storage:
            raise ValueError(f"Payee {payee.id} not found")
        self._storage[payee.id] = payee
