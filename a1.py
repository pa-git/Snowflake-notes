# 4. Lookup in rate card with flexible filters
mask = ratecard["vendor"] == vendor  # vendor is always required

if country:
    mask &= ratecard["country"] == country
if level:
    mask &= ratecard["level"] == level
if current_currency:
    mask &= ratecard["currency"] == current_currency

row = ratecard[mask]
