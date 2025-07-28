import random
import time

def payout_local_currency(amount: float, currency: str) -> dict:
    """
    Simulate a payout via stablecoin conversion to local fiat.
    """
    time.sleep(0.2)  # simulate network delay

    fx_rate = {
        "INR": 83.0,
        "NGN": 1500.0,
        "PHP": 58.0
    }.get(currency.upper(), 75.0)

    local_amount = round(amount * fx_rate, 2)

    return {
        "provider": "MockFX",
        "status": "paid_out",
        "amount": local_amount,
        "currency": currency.upper(),
        "payout_id": f"offramp_{random.randint(1000, 9999)}",
        "fx_rate": fx_rate
    }
