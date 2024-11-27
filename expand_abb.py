import re

abbreviation_map = {
    "mr": "mister",
    "dr": "doctor",
    "st": "street",
    "ave": "avenue",
    "dept": "department",
    "apt": "apartment",
    "etc": "et cetera"
}

def expand_abbreviations_with_regex(search_term, abbreviation_map):
    pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in abbreviation_map.keys()) + r')\b', re.IGNORECASE)
    return pattern.sub(lambda x: abbreviation_map[x.group().lower()], search_term)

search_term = "Dr. Smith Apt 4B St. Ave"
expanded_search_term = expand_abbreviations_with_regex(search_term, abbreviation_map)
print(f"Expanded: {expanded_search_term}")
