"""
LSTM Model Module.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, Dict, Any
import joblib

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False


class LSTMStockModel:
    """LSTM model for stock price prediction."""
    
    def __init__(self, look_back: int = 60, epochs: int = 50, batch_size: int = 32):
        """Initialize the model."""
        self.model = None
        self.scaler = None
        self.feature_columns = []
        self.target_column = 'close'
        self.is_fitted_ = False
        self.look_back = look_back
        self.epochs = epochs
        self.batch_size = batch_size
        
    def prepare_features(self, df: pd.DataFrame, target_col: str = 'close') -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for training with look-back window."""
        self.target_column = target_col
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
        
        data = df[feature_cols + [target_col]].dropna().values
        
        self.scaler = MinMaxScaler()
        scaled_data = self.scaler.fit_transform(data)
        
        X, y = [], []
        for i in range(self.look_back, len(scaled_data)):
            X.append(scaled_data[i-self.look_back:i])
            y.append(scaled_data[i, -1])
        
        return np.array(X), np.array(y)
    
    def train(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Train the LSTM model."""
        if not HAS_TENSORFLOW:
            raise ImportError("TensorFlow is not installed. Install with: pip install tensorflow")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, shuffle=False
        )
        
        self.model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        
        early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        
        self.model.fit(
            X_train, y_train,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_split=0.1,
            callbacks=[early_stop],
            verbose=0
        )
        
        y_pred = self.model.predict(X_test, verbose=0)
        y_pred = y_pred.flatten()
        
        # Inverse transform to original scale
        # Get the number of features from the scaler (includes target column)
        n_features = self.scaler.n_features_in_
        
        # Create arrays for inverse transform
        y_test_reshaped = y_test.reshape(-1, 1)
        y_pred_reshaped = y_pred.reshape(-1, 1)
        
        # Pad with zeros to match the number of features
        dummy_y_test = np.zeros((len(y_test_reshaped), n_features))
        dummy_y_pred = np.zeros((len(y_pred_reshaped), n_features))
        
        # Put the target values in the last column
        dummy_y_test[:, -1] = y_test_reshaped.flatten()
        dummy_y_pred[:, -1] = y_pred_reshaped.flatten()
        
        # Inverse transform
        y_test_actual = self.scaler.inverse_transform(dummy_y_test)[:, -1]
        y_pred_actual = self.scaler.inverse_transform(dummy_y_pred)[:, -1]
        
        # Calculate metrics on original scale
        mse_val = mean_squared_error(y_test_actual, y_pred_actual)
        rmse_val = np.sqrt(mse_val)
        mae_val = mean_absolute_error(y_test_actual, y_pred_actual)
        r2_val = r2_score(y_test_actual, y_pred_actual)
        
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
        return self.model.predict(X, verbose=0).flatten()
    
    def save_model(self, filepath: str):
        """Save model to file."""
        self.model.save(filepath.replace('.joblib', '.h5'))
        joblib.dump({
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'target_column': self.target_column,
            'look_back': self.look_back
        }, filepath)
    
    def load_model(self, filepath: str):
        """Load model from file."""
        from tensorflow.keras.models import load_model
        data = joblib.load(filepath)
        self.model = load_model(filepath.replace('.joblib', '.h5'))
        self.scaler = data['scaler']
        self.feature_columns = data['feature_columns']
        self.target_column = data.get('target_column', 'close')
        self.look_back = data['look_back']
        self.is_fitted_ = True
