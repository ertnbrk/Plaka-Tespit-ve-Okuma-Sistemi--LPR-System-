import os
import psycopg2
from sqlalchemy import create_engine

# Try both localhost and 127.0.0.1
urls = [
    "postgresql://postgres:password@localhost:5432/lpr_db",
    "postgresql://postgres:password@127.0.0.1:5432/lpr_db"
]

with open("debug_result.txt", "w", encoding="utf-8") as f:
    f.write("--- Testing DB Connectivity ---\n")

    for url in urls:
        f.write(f"\nTesting: {url}\n")
        try:
            engine = create_engine(url)
            with engine.connect() as conn:
                f.write("SUCCESS! Connected.\n")
        except Exception as e:
            f.write(f"FAILED: {e}\n")
