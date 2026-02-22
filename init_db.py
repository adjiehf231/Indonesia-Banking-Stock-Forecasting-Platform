"""
Script to initialize the database with all required tables.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager

def main():
    """Initialize the database."""
    print("Initializing database...")
    db = DatabaseManager()
    db.initialize_database()
    print("Database initialized successfully!")
    print("Tables created:")
    print("  - stocks_data")
    print("  - model_metrics")
    print("  - predictions")
    print("  - data_collection_log")

if __name__ == "__main__":
    main()
