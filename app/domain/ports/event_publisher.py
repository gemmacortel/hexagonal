from abc import ABC, abstractmethod

from app.domain.events.domain_event import DomainEvent


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, topic: str, event: DomainEvent) -> None:
        pass

