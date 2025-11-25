from dataclasses import asdict
from datetime import datetime
from uuid import UUID

from app.domain import PayeeOnboardedEvent
from app.domain.ports import PublishPayeeOnboardedEvent


class KafkaPublisher:
    def publish(self, topic: str, event_as_dict: dict) -> None:
        # sends to data
        pass


class KafkaPublishPayeeOnboardedEvent(PublishPayeeOnboardedEvent):
    def __init__(
            self,
            kafka_publisher: KafkaPublisher
    ):
        self.kafka_publisher = kafka_publisher

    def execute(self, event: PayeeOnboardedEvent) -> None:
        event_as_dict = self._event_to_dict(event)
        self.kafka_publisher.publish(topic="payee-topic", event_as_dict=event_as_dict)

    def _event_to_dict(self, event: PayeeOnboardedEvent) -> dict:
        data = asdict(event)

        for key, value in data.items():
            if isinstance(value, UUID):
                data[key] = str(value)
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
        return data


#class KafkaPublishPayeeDeletedEvent(PublishPayeeDeletedEvent):
#    def __init__(
#            self,
#            kafka_publisher: KafkaPublisher
#    ):
#        self.kafka_publisher = kafka_publisher
#
#    def execute(self, event: PayeeDeletedEvent) -> None:
#        pass

class MockPublishPayeeOnboardedEvent(PublishPayeeOnboardedEvent):

    def execute(self, event: PayeeOnboardedEvent) -> None:
        pass





