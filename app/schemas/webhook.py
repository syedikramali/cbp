from pydantic import BaseModel
from uuid import UUID
from enum import Enum

class EventType(str, Enum):
    payment_completed = "payment_completed"
    payment_failed = "payment_failed"

class WebhookEvent(BaseModel):
    transaction_id: UUID
    event_type: EventType
