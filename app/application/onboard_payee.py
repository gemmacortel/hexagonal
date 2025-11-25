from app.application.dtos import OnboardPayeeRequest, PayeeResponse
from app.domain.events import PayeeOnboardedEvent
from app.domain.model import Payee
from app.domain.ports import PublishPayeeOnboardedEvent, PayeeRepository, PSPClient


class OnboardPayeeService:
    def __init__(
        self,
        repository: PayeeRepository,
        psp_client: PSPClient,
        publish_payee_onboarded_event: PublishPayeeOnboardedEvent,
    ):
        self.repository = repository
        self.psp_client = psp_client
        self.publish_payee_onboarded_event = publish_payee_onboarded_event
    
    def execute(self, request: OnboardPayeeRequest) -> PayeeResponse:
        payee = Payee.create(
            name=request.name,
            email=request.email,
            bank_account=request.bank_account,
        )
        
        self.repository.save(payee)
        
        try:
            psp_reference = self.psp_client.onboard_payee(
                name=payee.name,
                email=payee.email,
                bank_account=payee.bank_account,
            )
            
            payee.set_psp_reference(psp_reference)
            payee.activate()
        except Exception:
            payee.mark_as_failed()
            self.repository.update(payee)
            raise

        self.repository.update(payee)

        event = PayeeOnboardedEvent.create(
            payee_id=payee.id,
            name=payee.name,
            email=payee.email,
            psp_reference=psp_reference,
            timestamp=payee.updated_at,
        )
        self.publish_payee_onboarded_event.execute(event)
        
        return PayeeResponse(
            id=payee.id,
            name=payee.name,
            email=payee.email,
            bank_account=payee.bank_account,
            status=payee.status.value,
            psp_reference=payee.psp_reference,
            created_at=payee.created_at,
            updated_at=payee.updated_at,
        )
