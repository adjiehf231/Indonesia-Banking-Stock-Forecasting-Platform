"""
Prediction API Module.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

from database.db_manager import DatabaseManager
from models.model_manager import ModelManager

logger = logging.getLogger(__name__)


class PredictionAPI:
    """API for making predictions."""
    
    def __init__(self, db_manager: DatabaseManager, models_dir: str = 'models'):
        """Initialize the prediction API."""
        self.db_manager = db_manager
        self.model_manager = ModelManager(models_dir)
        
    def _get_best_model(self, ticker: str) -> str:
        """Get the best model for a ticker, with fallback."""
        model_type = self.db_manager.get_best_model_name(ticker)
        if model_type is None:
            model_type = 'xgboost'
        return model_type
    
    def _calculate_trend(self, df: pd.DataFrame, days: int) -> float:
        """Calculate trend based on recent price movements."""
        if len(df) < 2:
            return 0.0
        
        # Calculate average daily change over recent period
        recent_data = df['close'].iloc[-min(days, len(df)):]
        if len(recent_data) < 2:
            return 0.0
        
        # Calculate daily returns
        returns = recent_data.pct_change().dropna()
        
        if len(returns) == 0:
            return 0.0
        
        # Average daily return
        avg_return = returns.mean()
        
        # Standard deviation for confidence
        std_return = returns.std()
        
        # Use weighted average with confidence adjustment
        # More recent days get higher weight
        weights = np.linspace(0.5, 1.5, len(returns))
        weighted_return = np.average(returns.values, weights=weights)
        
        return weighted_return
        
    def _calculate_volatility(self, df: pd.DataFrame, days: int = 30) -> float:
        """Calculate historical volatility."""
        if len(df) < 2:
            return 0.0
        
        recent_data = df['close'].iloc[-min(days, len(df)):]
        returns = recent_data.pct_change().dropna()
        
        if len(returns) == 0:
            return 0.0
        
        return returns.std()
    
    def predict(self, ticker: str, model_type: str = None) -> Dict[str, Any]:
        """
        Make a prediction for a given ticker.
        
        Args:
            ticker: Stock ticker symbol
            model_type: Type of model to use for prediction. If None, uses best model automatically.
            
        Returns:
            Dictionary with prediction results
        """
        df = self.db_manager.get_stock_data(ticker)
        
        if df.empty:
            return {'error': 'No data available for prediction'}
        
        # Auto-select best model if none specified
        if model_type is None:
            model_type = self._get_best_model(ticker)
        
        try:
            model = self.model_manager.load_model(ticker, model_type)
            
            if model is None:
                return {'error': f'Model not found for {ticker} {model_type}'}
            
            X, _ = model.prepare_features(df)
            prediction = model.predict(X[-1:])
            
            return {
                'ticker': ticker,
                'model_type': model_type,
                'predicted_price': float(prediction[0]),
                'current_price': float(df['close'].iloc[-1]),
                'prediction_date': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            return {'error': str(e)}
    
    def predict_future(self, ticker: str, days: int, model_type: str = None) -> List[Dict[str, Any]]:
        """
        Predict future prices for a given number of days using hybrid forecasting.
        
        Combines ML model predictions with trend-based forecasting for more realistic
        long-term predictions.
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days to predict
            model_type: Type of model to use. If None, uses best model automatically.
            
        Returns:
            List of prediction dictionaries
        """
        # Auto-select best model if none specified
        if model_type is None:
            model_type = self._get_best_model(ticker)
        
        # Get the model
        model = self.model_manager.load_model(ticker, model_type)
        if model is None:
            return []
        
        # Get historical data
        df = self.db_manager.get_stock_data(ticker)
        if df.empty:
            return []
        
        # Get current price and calculate trend
        current_price = float(df['close'].iloc[-1])
        
        # Calculate trend and volatility from historical data
        trend = self._calculate_trend(df, 30)  # 30-day trend
        volatility = self._calculate_volatility(df, 30)
        
        current_date = datetime.now()
        
        # Make a copy for iterative predictions
        df_pred = df.copy()
        
        predictions = []
        
        # Blend factor: starts high (favor ML model) and decreases over time
        # This gives more weight to ML model for short-term, trend for long-term
        for i in range(days):
            target_date = current_date + timedelta(days=i+1)
            
            # Day-based blend factor (linear decay over 30 days)
            blend_factor = max(0.2, 1.0 - (i / 30))
            
            try:
                # Get ML model prediction
                X, _ = model.prepare_features(df_pred)
                last_features = X.iloc[[-1]].copy()
                ml_pred = float(model.predict(last_features)[0])
                
                # Calculate trend-adjusted prediction
                days_ahead = i + 1
                # Apply trend with decay factor (trend becomes less reliable further out)
                trend_adjusted = current_price * ((1 + trend * blend_factor) ** days_ahead)
                
                # Blend ML prediction with trend
                final_pred = (blend_factor * ml_pred) + ((1 - blend_factor) * trend_adjusted)
                
                # Add some realistic variation based on volatility
                np.random.seed(i + int(datetime.now().timestamp()))
                noise = np.random.normal(0, volatility * current_price * 0.1)
                final_pred = final_pred + noise
                
                # Create prediction result
                pred_result = {
                    'ticker': ticker,
                    'model_type': model_type,
                    'predicted_price': float(final_pred),
                    'current_price': current_price,
                    'prediction_date': datetime.now().strftime('%Y-%m-%d'),
                    'target_date': target_date.strftime('%Y-%m-%d'),
                    'ml_prediction': float(ml_pred),
                    'trend_prediction': float(trend_adjusted)
                }
                predictions.append(pred_result)
                
                # Update the dataframe with the prediction for next iteration
                new_row = df_pred.iloc[-1].copy()
                new_row['close'] = final_pred
                new_row['date'] = target_date.strftime('%Y-%m-%d')
                
                # Recalculate key features
                window_5 = min(5, len(df_pred))
                window_10 = min(10, len(df_pred))
                window_20 = min(20, len(df_pred))
                
                if 'ma_5' in df_pred.columns:
                    new_row['ma_5'] = df_pred['close'].iloc[-window_5:].mean()
                if 'ma_10' in df_pred.columns:
                    new_row['ma_10'] = df_pred['close'].iloc[-window_10:].mean()
                if 'ma_20' in df_pred.columns:
                    new_row['ma_20'] = df_pred['close'].iloc[-window_20:].mean()
                
                # Append the new row
                df_pred = pd.concat([df_pred, pd.DataFrame([new_row])], ignore_index=True)
                
            except Exception as e:
                logger.error(f"Error in prediction at day {i+1}: {str(e)}")
                break
        
        return predictions
    
    def get_prediction_by_period(self, ticker: str, period: str) -> Dict[str, Any]:
        """
        Get predictions for a specific time period.
        
        Args:
            ticker: Stock ticker symbol
            period: Prediction period (1d, 3d, 1w, 2w, 1m, 3m, 6m, 9m, 1y, 2y)
            
        Returns:
            Dictionary with prediction results
        """
        period_map = {
            '1d': 1,
            '3d': 3,
            '1w': 7,
            '2w': 14,
            '1m': 30,
            '3m': 90,
            '6m': 180,
            '9m': 270,
            '1y': 365,
            '2y': 730
        }
        
        days = period_map.get(period, 1)
        
        # Get best model name for this ticker
        best_model = self._get_best_model(ticker)
        
        predictions = self.predict_future(ticker, days, best_model)
        
        if not predictions:
            return {'error': 'No predictions available'}
        
        final_pred = predictions[-1]
        
        return {
            'ticker': ticker,
            'period': period,
            'model_type': best_model,
            'current_price': final_pred.get('current_price'),
            'predicted_price': final_pred.get('predicted_price'),
            'predictions': predictions
        }
    
    def get_all_predictions(self, ticker: str) -> pd.DataFrame:
        """Get all saved predictions for a ticker."""
        return self.db_manager.get_predictions(ticker)
    
    def save_prediction(self, ticker: str, prediction_date: str, target_date: str,
                       predicted_price: float, model_name: str):
        """Save a prediction to the database."""
        self.db_manager.insert_prediction(
            ticker=ticker,
            prediction_date=prediction_date,
            target_date=target_date,
            predicted_price=predicted_price,
            model_name=model_name
        )
