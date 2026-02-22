"""Test script untuk debugging training model"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from models.model_manager import ModelManager

# Initialize
db = DatabaseManager()
model_manager = ModelManager()

# Get available tickers
tickers = db.get_all_tickers()
print(f"Available tickers: {tickers}")

if tickers:
    ticker = tickers[0]
    print(f"\n=== Testing training for {ticker} ===\n")
    
    # Get data
    df = db.get_stock_data(ticker)
    print(f"Data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    
    # Try to train all models
    print("\n=== Training all models ===")
    try:
        results = model_manager.train_all_models(df, ticker)
        print(f"\n=== Results ===")
        for model_name, metrics in results.items():
            print(f"{model_name}: {metrics}")
    except Exception as e:
        print(f"Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
