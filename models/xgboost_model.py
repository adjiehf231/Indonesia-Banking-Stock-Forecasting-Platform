"""
XGBoost Model Module.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict, Any
import joblib

try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False


class XGBoostStockModel:
    """XGBoost model for stock price prediction."""
    
    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.1, 
                 max_depth: int = 5, random_state: int = 42):
        """Initialize the model."""
        self.model = None
        self.scaler = None
        self.feature_columns = []
        self.is_fitted_ = False
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.random_state = random_state
        
    def prepare_features(self, df: pd.DataFrame, target_col: str = 'close') -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare features for training."""
        feature_cols = [
            'open', 'high', 'low', 'volume',
            'ma_5', 'ma_10', 'ma_20', 'ma_50',
            'ema_12', 'ema_26',
            'macd', 'macd_signal',
            'vwap', 'rsi',
            'stochastic_k', 'stochastic_d',
            'roc', 'bb_upper', 'bb_middle', 'bb_lower',
            'atr', 'volatility'
        ]
        feature_cols = [c for c in feature_cols if c in df.columns]
        self.feature_columns = feature_cols
        X = df[feature_cols].copy()
        y = df[target_col].copy()
        return X, y
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Train the model and return evaluation metrics."""
        if not HAS_XGBOOST:
            raise ImportError("XGBoost is not installed. Install with: pip install xgboost")
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.25, random_state=self.random_state
        )
        
        self.model = xgb.XGBRegressor(
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            max_depth=self.max_depth,
            random_state=self.random_state,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        mse_val = mean_squared_error(y_test, y_pred)
        rmse_val = np.sqrt(mse_val)
        mae_val = mean_absolute_error(y_test, y_pred)
        r2_val = r2_score(y_test, y_pred)
        
        metrics = {
            'mse': float(mse_val),
            'rmse': float(rmse_val),
            'mae': float(mae_val),
            'r2_score': float(r2_val)
        }
        self.is_fitted_ = True
        return metrics
    
    def predict(self, X):
        """Make predictions on new data."""
        if self.model is None or self.scaler is None:
            raise ValueError("Model not trained yet")
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def save_model(self, filepath: str):
        """Save model to file."""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }, filepath)
    
    def load_model(self, filepath: str):
        """Load model from file."""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_columns = data['feature_columns']
        self.is_fitted_ = True
