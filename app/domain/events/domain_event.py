from dataclasses import dataclass, asdict
from datetime import datetime
from uuid import UUID


@dataclass
class DomainEvent:
    def to_dict(self) -> dict:
        data = asdict(self)
        for key, value in data.items():
            if isinstance(value, UUID):
                data[key] = str(value)
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
        return data

