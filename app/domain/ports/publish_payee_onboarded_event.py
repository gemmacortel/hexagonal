from abc import ABC, abstractmethod

from app.domain import PayeeOnboardedEvent

class PublishPayeeOnboardedEvent(ABC):
    @abstractmethod
    def execute(self, event: PayeeOnboardedEvent) -> None:
        pass



