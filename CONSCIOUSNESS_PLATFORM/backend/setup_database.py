#!/usr/bin/env python3
"""
Database Setup Script
=====================
Quick setup for Consciousness Platform database.

Usage:
    python setup_database.py           # Interactive setup
    python setup_database.py --auto    # Auto-create tables (no migrations)
"""

import sys
import os
import argparse

def setup_with_migrations():
    """Setup database using Alembic migrations (recommended)"""
    print("=" * 60)
    print("DATABASE SETUP - Using Alembic Migrations")
    print("=" * 60)

    # Check if alembic is installed
    try:
        import alembic
    except ImportError:
        print("❌ Alembic not installed. Install it:")
        print("   pip install alembic")
        return False

    print("\n📦 Step 1: Create initial migration...")
    os.system("alembic revision --autogenerate -m 'Initial migration'")

    print("\n📦 Step 2: Apply migration to database...")
    os.system("alembic upgrade head")

    print("\n✅ Database setup complete!")
    print("\nNext steps:")
    print("  1. Update .env with your DATABASE_URL")
    print("  2. Run: python platform_api.py")
    print("  3. Test: curl http://localhost:5002/health")
    return True

def setup_without_migrations():
    """Setup database by creating tables directly (quick & dirty)"""
    print("=" * 60)
    print("DATABASE SETUP - Direct Table Creation")
    print("=" * 60)

    from models import init_db, DATABASE_URL

    print(f"\n📦 Database URL: {DATABASE_URL}")
    print("\n⚠️  Warning: This creates tables without migration tracking.")
    print("   For production, use Alembic migrations instead.\n")

    choice = input("Continue? (y/n): ")
    if choice.lower() != 'y':
        print("❌ Setup canceled")
        return False

    print("\n📦 Creating tables...")
    try:
        init_db()
        print("\n✅ Tables created successfully!")
        print("\nNext steps:")
        print("  1. Run: python platform_api.py")
        print("  2. Test: curl http://localhost:5002/health")
        return True
    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        print("\nTroubleshooting:")
        print("  1. Check DATABASE_URL in .env")
        print("  2. Ensure PostgreSQL is running")
        print("  3. Verify database credentials")
        return False

def main():
    parser = argparse.ArgumentParser(description="Setup Consciousness Platform database")
    parser.add_argument("--auto", action="store_true", help="Auto-create tables without migrations")
    parser.add_argument("--migrations", action="store_true", help="Use Alembic migrations (recommended)")
    args = parser.parse_args()

    if args.auto:
        return setup_without_migrations()
    elif args.migrations:
        return setup_with_migrations()
    else:
        # Interactive mode
        print("=" * 60)
        print("CONSCIOUSNESS PLATFORM - DATABASE SETUP")
        print("=" * 60)
        print("\nChoose setup method:")
        print("  1. Alembic migrations (recommended for production)")
        print("  2. Direct table creation (quick setup for development)")
        print("  3. Cancel")

        choice = input("\nYour choice (1-3): ")

        if choice == "1":
            return setup_with_migrations()
        elif choice == "2":
            return setup_without_migrations()
        else:
            print("❌ Setup canceled")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
