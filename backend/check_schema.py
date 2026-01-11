#!/usr/bin/env python3
"""Check database schema"""
from sqlalchemy import create_engine, inspect
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
inspector = inspect(engine)

print("=== Users Table Columns ===")
for column in inspector.get_columns('users'):
    print(f"  {column['name']}: {column['type']}")

print("\n=== Complaints Table Columns ===")
for column in inspector.get_columns('complaints'):
    print(f"  {column['name']}: {column['type']}")
