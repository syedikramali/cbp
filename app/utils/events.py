from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.transaction import Transaction, TransactionStatus
from app.schemas.webhook import WebhookEvent

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhooks")
def handle_webhook(event: WebhookEvent, db: Session = Depends(get_db)):
    
    """Handle incoming webhook events and update transaction status accordingly."""
    txn = db.query(Transaction).filter(Transaction.id == event.transaction_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Check if the transaction is already completed or failed    
    if txn.status == TransactionStatus.completed or txn.status == TransactionStatus.failed:
        return {"message": f"Transaction {txn.id} already in status {txn.status.value}"}
    
    if event.event_type == "payment_completed":
        txn.status = TransactionStatus.completed
    elif event.event_type == "payment_failed":
        txn.status = TransactionStatus.failed

    db.commit()
    return {"message": f"Transaction {txn.id} updated to {txn.status.value}"}
