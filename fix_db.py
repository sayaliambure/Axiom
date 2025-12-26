#!/usr/bin/env python3
"""
Database schema fix script for AXIOM.

This script will:
1. Drop all existing tables
2. Recreate them with the correct schema

WARNING: This will delete all data in the database!
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import inspect
from src.database import Base, engine
from src.db_models import User, Company, FinancialSnapshot, HireScenario

def check_tables():
    """Check which tables exist."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    return existing_tables

def drop_all_tables():
    """Drop all existing tables."""
    print("Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped")

def create_all_tables():
    """Create all tables with correct schema."""
    print("Creating all tables with correct schema...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created")

def main():
    """Main function."""
    print("=" * 60)
    print("AXIOM Database Schema Fix")
    print("=" * 60)
    
    # Check existing tables
    existing = check_tables()
    if existing:
        print(f"\nExisting tables: {', '.join(existing)}")
        print("\n⚠️  WARNING: This will delete all data in these tables!")
        response = input("Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return
    else:
        print("\nNo existing tables found.")
    
    # Drop and recreate
    print("\n" + "=" * 60)
    drop_all_tables()
    create_all_tables()
    
    # Verify
    print("\n" + "=" * 60)
    print("Verifying tables...")
    new_tables = check_tables()
    print(f"Created tables: {', '.join(new_tables)}")
    
    expected_tables = ['users', 'companies', 'financial_snapshots', 'hire_scenarios']
    for table in expected_tables:
        if table in new_tables:
            print(f"  ✅ {table}")
        else:
            print(f"  ❌ {table} - MISSING!")
    
    print("\n" + "=" * 60)
    print("✅ Database schema fixed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure PostgreSQL is running")
        print("  2. Verify database 'axiom' exists")
        print("  3. Check database credentials in src/database.py")
        sys.exit(1)

