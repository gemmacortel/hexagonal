from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class OnboardPayeeRequest(BaseModel):
    name: str
    email: EmailStr
    bank_account: str


class PayeeResponse(BaseModel):
    id: UUID
    name: str
    email: str
    bank_account: str
    status: str
    psp_reference: Optional[str]
    created_at: datetime
    updated_at: datetime
