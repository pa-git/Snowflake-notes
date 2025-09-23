# tools/ratecard_lookup_usd.py (patched)

from pydantic import BaseModel, Field, PrivateAttr
from crewai.tools import BaseTool
# ... keep the rest of your imports and helper code ...

class RatecardLookupTool(BaseTool):
    # Public metadata (fine to keep as class vars)
    name: str = "Rate Card Lookup"
    description: str = (
        "Retrieves vendor rate card data filtered by country, currency, role level, and vendor. "
        "Returns only the rows found (each with a 'usd_rate' column). "
        "If any filter value is invalid, returns an error and the allowed values."
    )
    args_schema: type = LookupInput
    return_direct: bool = False

    # >>> IMPORTANT: hold non-pydantic objects as a private attribute
    _store: "RatecardStore" = PrivateAttr()

    def __init__(self, store: "RatecardStore", **data):
        # initialize the pydantic/BaseTool bits first
        super().__init__(**data)
        # then attach your python object privately
        self._store = store

    def _run(self, **kwargs):
        args = LookupInput(**kwargs)

        # Validate against dynamic allowed values
        errors = self._store.validate_inputs(args.country, args.currency, args.level, args.vendor)
        if errors:
            return {
                "error": " | ".join(errors.values()),
                "allowed_values": self._store.allowed,
            }

        # Return only the rows
        df = self._store.lookup(
            country=args.country,
            currency=args.currency,
            level=args.level,
            vendor=args.vendor,
        )
        return df.to_dict(orient="records")


def make_lookup_tool(rate_card_csv: str = "rate_card.csv", fx_rates_csv: str = "fx-rates.csv") -> RatecardLookupTool:
    store = RatecardStore(rate_card_csv, fx_rates_csv)
    return RatecardLookupTool(store=store)
