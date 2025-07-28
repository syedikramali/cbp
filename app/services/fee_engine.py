def calculate_fee(amount: float, destination_currency: str) -> float:
    base_fee = 1.00
    percent_fee_map = {
        "INR": 0.02,
        "NGN": 0.03,
        "PHP": 0.015,
    }
    percentage = percent_fee_map.get(destination_currency.upper(), 0.025)
    return round(base_fee + amount * percentage, 2)
