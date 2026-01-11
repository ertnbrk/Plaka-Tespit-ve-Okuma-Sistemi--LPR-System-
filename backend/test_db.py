import os
import psycopg2
from sqlalchemy import create_engine

# Try both localhost and 127.0.0.1
urls = [
    "postgresql://postgres:password@localhost:5432/lpr_db",
    "postgresql://postgres:password@127.0.0.1:5432/lpr_db"
]

print("--- Testing DB Connectivity ---")

for url in urls:
    print(f"\nTesting: {url}")
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            print("SUCCESS! Connected.")
    except Exception as e:
        print(f"FAILED: {e}")
