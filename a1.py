import os, json
from dotenv import load_dotenv
from neomodel import db, config
from models import Role

load_dotenv()
config.DATABASE_URL = os.getenv("DATABASE_URL")

# --- Currency normalization and exchange ---
CURRENCY_NORMALIZATION = {
    "USD": "USD", "usd": "USD",
    "INR": "INR", "₹": "INR",
    "RMB": "CNY", "CNY": "CNY",
    "EUR": "EUR", "CAD": "CAD", "GBP": "GBP",
    "SGD": "SGD", "CHF": "CHF", "IDR": "IDR",
    "THB": "THB", "JPY": "JPY", "SAR": "SAR",
    "HUF": "HUF"
}

EXCHANGE_RATES_USD = {
    "USD": 1.0,
    "INR": 1 / 86.62,
    "CNY": 1 / 7.18,
    "EUR": 1.08,
    "CAD": 0.75,
    "GBP": 1.27,
    "SGD": 0.74,
    "CHF": 1.12,
    "IDR": 0.000063,
    "THB": 0.027,
    "JPY": 0.0064,
    "SAR": 0.27,
    "HUF": 0.0028,
}

# --- Rate period conversion to hourly multiplier ---
RATE_PERIOD_TO_HOURLY = {
    "hourly": 1,
    "daily": 1 / 8,
    "weekly": 1 / 40,
    "monthly": 1 / 160,
    "annually": 1 / 1920,
    "annual": 1 / 1920,
    "total": 1,  # No scaling applied
    "project": 1,  # Assume entire project is 1 fee
    "initial period fee": 1,
    "perlocation": 1,
    "2 hours + travel": 1 / 2  # Estimate as 2 hours only
}

def normalize_currency(currency):
    if not currency:
        raise ValueError("No currency provided")
    key = currency.strip().upper()
    norm = CURRENCY_NORMALIZATION.get(key)
    if not norm:
        raise ValueError(f"Unsupported currency: {currency}")
    return norm

def convert_to_usd(amount, raw_currency):
    curr = normalize_currency(raw_currency)
    rate = EXCHANGE_RATES_USD.get(curr)
    if rate is None:
        raise ValueError(f"No USD rate for: {curr}")
    return amount * rate

def convert_to_hourly(rate, period):
    if not period:
        raise ValueError("Missing rate period")
    key = period.strip().lower()
    if key not in RATE_PERIOD_TO_HOURLY:
        raise ValueError(f"Unsupported rate period: {period}")
    return rate * RATE_PERIOD_TO_HOURLY[key]

def standardize_role_rates():
    query = """
    MATCH (r:Role)
    RETURN r.uid AS uid, r.rate AS rate,
           r.rate_period AS period, r.rate_currency AS currency,
           r.total_fees AS fees
    """
    results, _ = db.cypher_query(query)
    output = []

    for uid, rate, period, currency, fees in results:
        try:
            if not currency or currency.lower() == "percent":
                raise ValueError("Invalid currency unit")

            rate_f = float(rate or 0)
            fees_f = float(fees or 0)

            hourly_usd = convert_to_usd(convert_to_hourly(rate_f, period), currency)
            fees_usd = convert_to_usd(fees_f, currency)

            output.append({
                "uid": uid,
                "hourly_rate_usd": round(hourly_usd, 2),
                "total_fees_usd": round(fees_usd, 2)
            })

        except Exception as e:
            print(f"⚠️ Skipped UID {uid} due to error: {e}")

    print(json.dumps(output, indent=2))
    return output

if __name__ == "__main__":
    standardize_role_rates()
