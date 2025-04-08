import re
import unicodedata

def slugify_filename(name: str) -> str:
    # Remove leading numbers and dots (e.g., "2. ")
    name = re.sub(r"^\d+\.\s*", "", name)
    # Normalize unicode characters (e.g., é → e)
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    # Replace non-alphanumeric with dashes
    name = re.sub(r"[^\w\s-]", "", name)
    # Replace spaces and underscores with single dash
    name = re.sub(r"[\s_]+", "-", name)
    # Convert to lowercase
    name = name.lower()
    # Strip leading/trailing dashes
    return name.strip("-")
