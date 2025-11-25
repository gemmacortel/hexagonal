from abc import ABC, abstractmethod


class PSPClient(ABC):
    @abstractmethod
    def onboard_payee(
        self,
        name: str,
        email: str,
        bank_account: str,
    ) -> str:
        pass

