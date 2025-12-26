#!/usr/bin/env python3
"""
Database initialization script for AXIOM.

Creates all database tables if they don't exist.
Run this once before starting the API server.

Usage:
    python init_db.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import Base, engine
# Import all models so SQLAlchemy registers them
from src.db_models import User, Company, FinancialSnapshot, HireScenario

def init_db():
    """Create all database tables."""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("\nTables created:")
        print("  - users")
        print("  - companies")
        print("  - financial_snapshots")
        print("  - hire_scenarios")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure PostgreSQL is running")
        print("  2. Verify database 'axiom' exists")
        print("  3. Check database credentials in src/database.py")
        sys.exit(1)

if __name__ == "__main__":
    init_db()

