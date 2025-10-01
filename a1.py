# vendor, country, currency must match
mask = (
    (ratecard["vendor"] == vendor)
    & (ratecard["country"] == country)
    & (ratecard["currency"] == current_currency)
)

# level: conditional
if level:
    mask &= ratecard["level"] == level
else:
    mask &= ratecard["level"] == ""  # match only rows where level is also empty

row = ratecard[mask]
