from dotenv import load_dotenv
from neomodel import config, db
import os

load_dotenv()
config.DATABASE_URL = os.getenv("DATABASE_URL")

try:
    results, _ = db.cypher_query("RETURN 'Connection successful' AS message")
    print("✅", results[0][0])
except Exception as e:
    print("❌ Connection failed:", e)
