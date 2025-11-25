from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.model.payee import Payee


class PayeeRepository(ABC):
    @abstractmethod
    def save(self, payee: Payee) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, payee_id: UUID) -> Optional[Payee]:
        pass
    
    @abstractmethod
    def update(self, payee: Payee) -> None:
        pass

