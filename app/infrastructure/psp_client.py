from uuid import uuid4

from app.domain.ports import PSPClient


class MockPSPClient(PSPClient):
    def onboard_payee(
        self,
        name: str,
        email: str,
        bank_account: str,
    ) -> str:
        psp_reference = f"PSP-{uuid4().hex[:12].upper()}"
        return psp_reference


class HTTPPSPClient(PSPClient):
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
    
    def onboard_payee(
        self,
        name: str,
        email: str,
        bank_account: str,
    ) -> str:
        raise NotImplementedError("Replace with actual HTTP implementation")
