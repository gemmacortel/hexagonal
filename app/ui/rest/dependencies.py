from functools import lru_cache

from app.application.onboard_payee_service import OnboardPayeeService
from app.infrastructure.database import InMemoryPayeeRepository
from app.infrastructure.psp_client import MockPSPClient
from app.infrastructure.pubsub import MockEventPublisher


@lru_cache
def get_payee_repository():
    return InMemoryPayeeRepository()


@lru_cache
def get_psp_client():
    return MockPSPClient()


@lru_cache
def get_event_publisher():
    return MockEventPublisher()


def get_onboard_payee_service() -> OnboardPayeeService:
    return OnboardPayeeService(
        repository=get_payee_repository(),
        psp_client=get_psp_client(),
        event_publisher=get_event_publisher(),
    )
