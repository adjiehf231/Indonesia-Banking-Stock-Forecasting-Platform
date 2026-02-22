"""
Debug script to test data collection.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from data.collect_data import fetch_stock_data
from data.indicators import calculate_all_indicators
from database.db_manager import DatabaseManager

# Test fetching one stock
print("Testing fetch for BMRI...")
df = fetch_stock_data('BMRI', '2022-01-01', '2026-02-22')
print(f"Raw data columns: {df.columns.tolist()}")
print(f"Raw data shape: {df.shape}")
print(df.head(2))

# Test indicators
print("\nCalculating indicators...")
df_with_indicators = calculate_all_indicators(df)
print(f"With indicators columns: {df_with_indicators.columns.tolist()}")
print(f"With indicators shape: {df_with_indicators.shape}")

# Test database insert
print("\nTesting database insert...")
db = DatabaseManager()
db.initialize_database()

# Get column names from database
conn = db.get_connection()
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(stocks_data)")
columns = cursor.fetchall()
print(f"Database columns: {[col[1] for col in columns]}")
conn.close()

# Count columns
print(f"Number of database columns (excluding id): {len([col[1] for col in columns]) - 1}")  # -1 for id
print(f"Number of columns in df: {len(df_with_indicators.columns)}")
