from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos import (
    OnboardPayeeRequest,
    PayeeResponse,
)
from app.application.onboard_payee import OnboardPayeeService
from app.domain.exceptions import DomainException
from app.ui.rest.dependencies import get_onboard_payee_service

router = APIRouter(prefix="/api/payees", tags=["payees"])


@router.post(
    "",
    response_model=PayeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Onboard a new payee",
    description="Creates a new payee, validates eligibility, onboards in PSP, and publishes event",
)
def onboard_payee(
    request: OnboardPayeeRequest,
    service: OnboardPayeeService = Depends(get_onboard_payee_service),
) -> PayeeResponse:
    try:
        payee = service.execute(request)
        return payee
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to onboard payee: {str(e)}",
        )
