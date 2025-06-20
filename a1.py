import os
from dotenv import load_dotenv
from neomodel import db, config
from models import Role

# Load environment
load_dotenv()
config.DATABASE_URL = os.getenv("DATABASE_URL")

# Normalize currencies
CURRENCY_NORMALIZATION = {
    "USD": "USD", "usd": "USD",
    "INR": "INR", "₹": "INR",
    "RMB": "CNY", "CNY": "CNY",
    "EUR": "EUR", "CAD": "CAD", "GBP": "GBP",
    "SGD": "SGD", "CHF": "CHF", "IDR": "IDR",
    "THB": "THB", "JPY": "JPY", "SAR": "SAR",
    "HUF": "HUF"
}

# Mid-market USD exchange rates (June 2025)
EXCHANGE_RATES = {
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

# Hours per period
PERIOD_MULTIPLIERS = {
    "Hourly": 1,
    "Daily": 1 / 8,
    "Weekly": 1 / 40,
    "Monthly": 1 / 160,
    "Annually": 1 / 1920,
    "2 hours + travel": 1 / 8,
    "Initial Period Fee": 1,
    "Total": 1,
    "PerLocation": 1,
    "Project": 1
}

def normalize_currency(curr):
    if not curr:
        raise ValueError("Missing currency")
    curr = curr.strip().upper()
    norm = CURRENCY_NORMALIZATION.get(curr)
    if not norm:
        raise ValueError(f"Unsupported currency: {curr}")
    return norm

def to_usd(amount, currency):
    currency = normalize_currency(currency)
    rate = EXCHANGE_RATES.get(currency)
    if rate is None:
        raise ValueError(f"No USD exchange rate for: {currency}")
    return amount * rate

def to_hourly(rate, period):
    period = (period or "").strip()
    mult = PERIOD_MULTIPLIERS.get(period)
    if mult is None:
        raise ValueError(f"Unsupported rate period: {period}")
    return rate * mult

def standardize_roles():
    roles = Role.nodes.all()
    updated = 0
    skipped = 0

    for r in roles:
        try:
            # Inputs
            rate = float(r.rate) if r.rate else 0.0
            total_fees = float(r.total_fees) if r.total_fees else 0.0
            currency = r.rate_currency
            period = r.rate_period

            if not currency or currency.lower() == "percent":
                raise ValueError("Invalid or unsupported currency format")

            # Compute USD values
            hourly_usd = to_usd(to_hourly(rate, period), currency)
            fees_usd = to_usd(total_fees, currency)

            # Update Role node
            r.standardized_hourly_rate = round(hourly_usd, 2)
            r.standardized_total_fees = round(fees_usd, 2)
            r.save()
            print(f"✅ Updated role {r.uid}")
            updated += 1

        except Exception as e:
            print(f"⚠️ Skipped role {r.uid if 'r' in locals() else 'Unknown'}: {e}")
            skipped += 1

    print(f"\n🏁 Done. {updated} roles updated, {skipped} skipped.")

if __name__ == "__main__":
    standardize_roles()
