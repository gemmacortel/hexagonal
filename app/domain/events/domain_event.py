from dataclasses import dataclass


@dataclass
class DomainEvent:
    event_type: str
