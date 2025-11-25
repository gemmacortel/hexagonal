from app.domain.events import DomainEvent
from app.domain.ports import EventPublisher


class MockEventPublisher(EventPublisher):
    def publish(self, topic: str, event: DomainEvent) -> None:
        event_data = event.to_dict()
        pass


class GCPPubSubEventPublisher(EventPublisher):
    def __init__(self, project_id: str):
        self.project_id = project_id
    
    def publish(self, topic: str, event: DomainEvent) -> None:
        raise NotImplementedError("Replace with actual GCP Pub/Sub implementation")
