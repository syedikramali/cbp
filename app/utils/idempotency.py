from app.models.transaction import Transaction
from sqlalchemy.orm import Session

def get_existing_transaction(db: Session, idempotency_key: str):
    return db.query(Transaction).filter(Transaction.idempotency_key == idempotency_key).first()
