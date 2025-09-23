# tools/ratecard_lookup_usd.py
from __future__ import annotations
from typing import Dict, Any
import re
import pandas as pd
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


# --------------------------- CSV Loaders ---------------------------

def _parse_rate_to_float(v) -> float:
    """Parses numbers or ranges like '238-245' into a float (midpoint)."""
    if v is None:
        return float("nan")
    if isinstance(v, (int, float)):
        return float(v)

    s = str(v).strip()
    if s.lower() in {"n/a", "na", ""}:
        return float("nan")

    s = s.replace("–", "-").replace("—", "-")
    m = re.match(r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$", s)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        return (a + b) / 2.0

    try:
        return float(s)
    except ValueError:
        return float("nan")


def load_ratecard(path: str) -> pd.DataFrame:
    """
    Expects columns (case-insensitive):
      country,currency,level,vendor,rate
    """
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    req = {"country", "currency", "level", "vendor", "rate"}
    miss = req - set(df.columns)
    if miss:
        raise ValueError(f"rate_card.csv missing columns: {sorted(miss)}")

    for col in ["country", "currency", "level", "vendor"]:
        df[col] = df[col].astype(str).str.strip()

    df["rate"] = df["rate"].apply(_parse_rate_to_float)
    df = df[~df["rate"].isna()].reset_index(drop=True)
    return df


def load_fx_table(path: str) -> pd.DataFrame:
    """
    Expects columns (case-insensitive): SOURCE_CURRENCY, TARGET_CURRENCY, RATE
    Assumes: 1 SOURCE = RATE * TARGET (so for USD→CAD, if RATE=1.392975 then 1 USD=1.392975 CAD).
    """
    fx = pd.read_csv(path)
    fx.columns = [c.strip().upper() for c in fx.columns]
    req = {"SOURCE_CURRENCY", "TARGET_CURRENCY", "RATE"}
    miss = req - set(fx.columns)
    if miss:
        raise ValueError(f"fx-rates.csv missing columns: {sorted(miss)}")

    for col in ["SOURCE_CURRENCY", "TARGET_CURRENCY"]:
        fx[col] = (
            fx[col].astype(str).str.strip().str.upper()
            .str.replace('"', "", regex=False).str.replace("'", "", regex=False)
        )

    fx = fx[fx["SOURCE_CURRENCY"] == "USD"].copy()
    fx["RATE"] = pd.to_numeric(
        fx["RATE"].astype(str).str.replace(",", "", regex=False).str.strip(),
        errors="coerce"
    )
    fx = fx.dropna(subset=["RATE"])
    return fx.rename(columns={"TARGET_CURRENCY": "currency", "RATE": "usd_to_curr"})[
        ["currency", "usd_to_curr"]
    ]


def attach_usd_rate(rates: pd.DataFrame, fx: pd.DataFrame) -> pd.DataFrame:
    """Adds a 'usd_rate' column. If currency==USD, usd_rate=rate; else usd_rate = rate / usd_to_curr."""
    fx_map = fx.set_index("currency")["usd_to_curr"].to_dict()

    def to_usd(row):
        cur = str(row["currency"]).upper()
        val = row["rate"]
        if pd.isna(val):
            return float("nan")
        if cur == "USD":
            return float(val)
        r = fx_map.get(cur)
        if r and r != 0:
            return float(val) / float(r)
        return float("nan")

    out = rates.copy()
    out["currency"] = out["currency"].str.upper()
    out["usd_rate"] = out.apply(to_usd, axis=1)
    return out


# --------------------------- In-memory store ---------------------------

class RatecardStore:
    """
    Keeps the loaded rate card (with `usd_rate`) and dynamic allowed values.
    """
    def __init__(self, rate_card_csv: str, fx_rates_csv: str):
        base = load_ratecard(rate_card_csv)
        fx = load_fx_table(fx_rates_csv)
        self.df = attach_usd_rate(base, fx)

        # dynamic allowed lists (exact values present in the file)
        self.allowed = {
            "country": sorted(self.df["country"].dropna().unique().tolist()),
            "currency": sorted(self.df["currency"].dropna().unique().tolist()),
            "level":    sorted(self.df["level"].dropna().unique().tolist()),
            "vendor":   sorted(self.df["vendor"].dropna().unique().tolist()),
        }

    def validate_inputs(self, country: str, currency: str, level: str, vendor: str) -> Dict[str, str]:
        """
        Returns a dict of {field: error_message} for invalid (non-empty) inputs.
        """
        errors: Dict[str, str] = {}
        if country and country not in self.allowed["country"]:
            errors["country"] = f"Invalid country '{country}'. Allowed: {', '.join(self.allowed['country'])}"
        if currency and currency.upper() not in self.allowed["currency"]:
            errors["currency"] = f"Invalid currency '{currency}'. Allowed: {', '.join(self.allowed['currency'])}"
        if level and level not in self.allowed["level"]:
            errors["level"] = f"Invalid level '{level}'. Allowed: {', '.join(self.allowed['level'])}"
        if vendor and vendor not in self.allowed["vendor"]:
            errors["vendor"] = f"Invalid vendor '{vendor}'. Allowed: {', '.join(self.allowed['vendor'])}"
        return errors

    def lookup(self, country: str, currency: str, level: str, vendor: str) -> pd.DataFrame:
        s = self.df
        if country:
            s = s[s["country"] == country]
        if currency:
            s = s[s["currency"] == currency.upper()]
        if level:
            s = s[s["level"] == level]
        if vendor:
            s = s[s["vendor"] == vendor]
        return s[["vendor", "level", "country", "currency", "rate", "usd_rate"]].reset_index(drop=True)


# --------------------------- CrewAI Tool ---------------------------

class LookupInput(BaseModel):
    country: str = Field("", description="Country filter. Leave empty for no filter.")
    currency: str = Field("", description="Currency filter (e.g., USD, CAD). Leave empty for no filter.")
    level: str = Field("", description="Role level filter. Leave empty for no filter.")
    vendor: str = Field("", description="Vendor filter. Leave empty for no filter.")


class RatecardLookupTool(BaseTool):
    name: str = "Rate Card Lookup"
    description: str = (
        "Retrieves vendor rate card data filtered by country, currency, role level, and vendor. "
        "Returns only the rows found (each with a 'usd_rate' column). "
        "If any filter value is invalid, returns an error and the allowed values."
    )
    args_schema: type = LookupInput
    return_direct: bool = False

    def __init__(self, store: RatecardStore, **data):
        super().__init__(**data)
        self.store = store

    def _run(self, **kwargs) -> Any:
        args = LookupInput(**kwargs)

        # Strict validation against dynamic allowed values; return error if any invalid
        errors = self.store.validate_inputs(args.country, args.currency, args.level, args.vendor)
        if errors:
            # One structured error message + include the allowed values for recovery
            return {
                "error": " | ".join(errors.values()),
                "allowed_values": self.store.allowed,
            }

        # Success → return just the rows (list of dicts)
        df = self.store.lookup(
            country=args.country,
            currency=args.currency,
            level=args.level,
            vendor=args.vendor,
        )
        return df.to_dict(orient="records")


# --------------------------- Helper to build the tool ---------------------------

def make_lookup_tool(rate_card_csv: str = "rate_card.csv", fx_rates_csv: str = "fx-rates.csv") -> RatecardLookupTool:
    store = RatecardStore(rate_card_csv, fx_rates_csv)
    return RatecardLookupTool(store=store)

# --------------------------- Import and build the tool ---------------------------

from tools.ratecard_lookup_usd import make_lookup_tool

# Initialize the tool from your CSVs
lookup_tool = make_lookup_tool(
    rate_card_csv="rate_card.csv",   # your vendor rate card file
    fx_rates_csv="fx-rates.csv"      # your FX rates file
)

# --------------------------- Call it directly in Python ---------------------------

# Example 1: valid filters
result = lookup_tool.run(country="US", currency="USD", level="Manager", vendor="EY")
print(result)
# → list of row dicts, e.g.:
# [
#   {"vendor": "EY", "level": "Manager", "country": "US", "currency": "USD", "rate": 250, "usd_rate": 250.0},
#   ...
# ]

# Example 2: invalid input
result = lookup_tool.run(country="Mars", currency="USD", level="", vendor="")
print(result)
# → {
#     "error": "Invalid country 'Mars'. Allowed: Canada, France, Germany, ...",
#     "allowed_values": {
#         "country": ["US","Canada",...],
#         "currency": ["USD","CAD",...],
#         "level": ["Staff","Associate",...],
#         "vendor": ["EY","KPMG","Accenture","PWC"]
#     }
#   }

# --------------------------- Register the tool with your CrewAI agent ---------------------------

from crewai import Agent

analyst = Agent(
    role="Analyst",
    goal="Answer questions about vendor rate cards.",
    backstory="Knows how to look up rates in different countries and normalize them to USD.",
    tools=[lookup_tool],   # register the tool
)

# Example agent call
response = analyst("What is the USD rate for a Manager in the US at EY?")
print(response)


