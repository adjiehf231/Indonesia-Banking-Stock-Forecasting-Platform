"""Test recursive forecasting."""
from api.predict_api import PredictionAPI
from database.db_manager import DatabaseManager

db = DatabaseManager()
api = PredictionAPI(db)

# Test different periods
print("Testing recursive forecasting with different periods:")
print("=" * 60)

for period in ['1d', '1w', '1m', '3m']:
    result = api.get_prediction_by_period('BBCA', period)
    if 'error' not in result:
        print(f"\nPeriod: {period}")
        print(f"  Current price: Rp {result['current_price']:,.0f}")
        print(f"  Predicted price: Rp {result['predicted_price']:,.0f}")
        print(f"  Model: {result.get('model_type', 'N/A')}")
        
        # Show first and last prediction
        preds = result.get('predictions', [])
        if preds:
            print(f"  First day prediction: Rp {preds[0]['predicted_price']:,.0f}")
            print(f"  Last day prediction: Rp {preds[-1]['predicted_price']:,.0f}")
