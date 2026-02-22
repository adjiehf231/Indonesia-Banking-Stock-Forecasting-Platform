"""
Script to collect stock data for all Indonesian banks.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from data.collect_data import fetch_and_save_all_banks

def main():
    """Collect and save stock data for all banks."""
    print("Initializing database...")
    db = DatabaseManager()
    db.initialize_database()
    
    print("\nCollecting stock data for 10 Indonesian banks...")
    print("This may take a few minutes...")
    
    results = fetch_and_save_all_banks(db, start_date='2022-01-01')
    
    print("\n" + "="*50)
    print("Data Collection Summary:")
    print("="*50)
    
    total_records = 0
    for bank_code, count in results.items():
        print(f"  {bank_code}: {count} records")
        total_records += count
    
    print("-"*50)
    print(f"Total records collected: {total_records}")
    print("="*50)
    
    if total_records > 0:
        print("\n✓ Data collection completed successfully!")
        print("You can now view the data in the Streamlit app.")
    else:
        print("\n✗ No data was collected. Please check your internet connection.")

if __name__ == "__main__":
    main()
