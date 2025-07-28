import random
import time

def collect_usd(amount: float) -> dict:
    """
    Simulate a USD collection step via a provider like Stripe or Circle.
    """
    time.sleep(0.2)  # simulate network delay
    return {
        "provider": "MockStripe",
        "status": "succeeded",
        "amount_collected": amount,
        "txn_id": f"onramp_{random.randint(1000, 9999)}"
    }
