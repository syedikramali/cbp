from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal
from enum import Enum
from datetime import datetime

class TransactionStatus(str, Enum):
    initiated = "initiated"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class PaymentRequest(BaseModel):
    user_id: UUID
    amount_usd: Decimal
    destination_currency: str

class PaymentResponse(BaseModel):
    id: UUID
    status: TransactionStatus
    fee: Decimal
    total_payout: Decimal
    created_at: datetime
    # Optional: mock integration tracking
    onramp_txn_id: str
    onramp_provider: str
    offramp_payout_id: str
    offramp_provider: str
    fx_rate: float
