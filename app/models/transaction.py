from sqlalchemy import Column, String, Numeric, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime
from app.db.base import Base
import enum

class TransactionStatus(str, enum.Enum):
    initiated = "initiated"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    amount_usd = Column(Numeric(10, 2), nullable=False)
    destination_currency = Column(String, nullable=False)
    fee = Column(Numeric(10, 2), nullable=False)
    total_payout = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.initiated)
    idempotency_key = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Optional: mock integration tracking
    onramp_txn_id = Column(String, nullable=True)
    onramp_provider = Column(String, nullable=True)

    offramp_payout_id = Column(String, nullable=True)
    offramp_provider = Column(String, nullable=True)

    fx_rate = Column(Numeric(10, 4), nullable=True)
