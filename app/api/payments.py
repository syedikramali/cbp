from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.transaction import Transaction
from app.schemas.payment import PaymentRequest, PaymentResponse, TransactionStatus
from app.services.fee_engine import calculate_fee
from app.services.onramp import collect_usd
from app.services.offramp import payout_local_currency
from app.utils.idempotency import get_existing_transaction

from uuid import UUID
from decimal import Decimal
from datetime import datetime


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/payments", response_model=PaymentResponse, status_code=201)
def create_payment(
    payload: PaymentRequest,
    idempotency_key: str = Header(...),
    db: Session = Depends(get_db)
):
    # Check for idempotency
    existing = get_existing_transaction(db, idempotency_key)
    if existing:
        return existing
    

    fee = Decimal(calculate_fee(float(payload.amount_usd), payload.destination_currency))
    total_payout = payload.amount_usd - fee
    
     # Mock USD collection
    onramp_result = collect_usd(float(payload.amount_usd))
    if onramp_result["status"] != "succeeded":
        raise HTTPException(status_code=400, detail="Onramp failed")

    # Mock local payout
    offramp_result = payout_local_currency(float(total_payout), payload.destination_currency)
    if offramp_result["status"] != "paid_out":
        raise HTTPException(status_code=400, detail="Offramp failed")

    new_txn = Transaction(
        user_id=payload.user_id,
        amount_usd=payload.amount_usd,
        destination_currency=payload.destination_currency,
        fee=fee,
        total_payout=total_payout,
        status=TransactionStatus.processing,
        idempotency_key=idempotency_key,
        created_at=datetime.utcnow(),
        # Optional: mock integration tracking
        onramp_txn_id=onramp_result["txn_id"],
        onramp_provider=onramp_result["provider"],
        offramp_payout_id=offramp_result["payout_id"],
        offramp_provider=offramp_result["provider"],
        fx_rate=offramp_result["fx_rate"]
    )

    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)

    return new_txn

@router.get("/payments/{transaction_id}")
def get_transaction_status(transaction_id: UUID, db: Session = Depends(get_db)):
    txn = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": txn.id,
        "status": txn.status,
        "total_payout": txn.total_payout,
        "currency": txn.destination_currency
    }
