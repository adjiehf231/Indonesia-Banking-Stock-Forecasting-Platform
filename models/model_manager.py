"""
Model Manager Module - Manages all ML models.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import os
import joblib
from datetime import datetime

from models.random_forest import RandomForestStockModel
from models.xgboost_model import XGBoostStockModel
from models.lstm_model import LSTMStockModel


class ModelManager:
    """Manages all machine learning models for stock prediction."""
    
    MODEL_TYPES = {
        'random_forest': RandomForestStockModel,
        'xgboost': XGBoostStockModel,
        'lstm': LSTMStockModel
    }
    
    def __init__(self, models_dir: str = 'models'):
        """Initialize the model manager."""
        self.models_dir = models_dir
        self.models: Dict[str, Any] = {}
        self.trained_tickers: List[str] = []
        
    def get_model(self, model_type: str):
        """Get a model instance by type."""
        if model_type not in self.MODEL_TYPES:
            raise ValueError(f"Unknown model type: {model_type}. Available: {list(self.MODEL_TYPES.keys())}")
        return self.MODEL_TYPES[model_type]()
    
    def train_all_models(self, df: pd.DataFrame, ticker: str) -> Dict[str, Dict[str, float]]:
        """
        Train all models on the given data.
        
        Args:
            df: DataFrame with stock data and features
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with model names and their metrics
        """
        results = {}
        
        for model_type, model_class in self.MODEL_TYPES.items():
            try:
                print(f"Training {model_type} for {ticker}...")
                
                model = model_class()
                X, y = model.prepare_features(df)
                
                # Handle NaN values - drop rows with NaN
                if hasattr(X, 'dropna'):
                    # For pandas DataFrame
                    X_clean = X.dropna()
                    y_clean = y.loc[X_clean.index]
                else:
                    # For numpy arrays
                    mask = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
                    X_clean = X[mask]
                    y_clean = y[mask]
                
                if len(X_clean) < 10:
                    print(f"Error: Insufficient data after cleaning: only {len(X_clean)} samples")
                    results[model_type] = {'error': f'Insufficient data: only {len(X_clean)} samples'}
                    continue
                
                metrics = model.train(X_clean, y_clean)
                results[model_type] = metrics
                
                self.models[f"{ticker}_{model_type}"] = model
                
                self.save_model(model, ticker, model_type)
                
                print(f"{model_type} trained successfully. Metrics: {metrics}")
                
            except Exception as e:
                print(f"Error training {model_type}: {str(e)}")
                results[model_type] = {'error': str(e)}
        
        if ticker not in self.trained_tickers:
            self.trained_tickers.append(ticker)
        
        return results
    
    def save_model(self, model, ticker: str, model_type: str):
        """Save a model to disk."""
        os.makedirs(self.models_dir, exist_ok=True)
        filepath = os.path.join(self.models_dir, f"{ticker}_{model_type}.joblib")
        model.save_model(filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, ticker: str, model_type: str):
        """Load a model from disk."""
        filepath = os.path.join(self.models_dir, f"{ticker}_{model_type}.joblib")
        
        if not os.path.exists(filepath):
            return None
        
        model = self.MODEL_TYPES[model_type]()
        model.load_model(filepath)
        
        self.models[f"{ticker}_{model_type}"] = model
        return model
    
    def predict(self, df: pd.DataFrame, ticker: str, model_type: str = 'xgboost') -> np.ndarray:
        """
        Make predictions using the specified model.
        
        Args:
            df: DataFrame with features
            ticker: Stock ticker
            model_type: Type of model to use
            
        Returns:
            Array of predictions
        """
        key = f"{ticker}_{model_type}"
        
        if key not in self.models:
            model = self.load_model(ticker, model_type)
            if model is None:
                raise ValueError(f"Model not found for {ticker} {model_type}")
        else:
            model = self.models[key]
        
        if model_type == 'lstm':
            X, _ = model.prepare_features(df)
        else:
            X, _ = model.prepare_features(df)
        
        return model.predict(X)
    
    def get_best_model(self, metrics: Dict[str, Dict[str, float]]) -> str:
        """
        Get the best model based on R2 score.
        
        Args:
            metrics: Dictionary with model metrics
            
        Returns:
            Name of the best model
        """
        best_model = None
        best_r2 = -np.inf
        
        for model_name, model_metrics in metrics.items():
            if 'r2_score' in model_metrics:
                r2 = model_metrics['r2_score']
                if r2 > best_r2:
                    best_r2 = r2
                    best_model = model_name
        
        return best_model
    
    def get_all_metrics(self, ticker: str) -> Dict[str, Dict[str, float]]:
        """Get metrics for all trained models for a ticker."""
        metrics = {}
        
        for model_type in self.MODEL_TYPES.keys():
            filepath = os.path.join(self.models_dir, f"{ticker}_{model_type}.joblib")
            if os.path.exists(filepath):
                try:
                    model = self.MODEL_TYPES[model_type]()
                    model.load_model(filepath)
                    metrics[model_type] = {'loaded': True}
                except:
                    metrics[model_type] = {'loaded': False}
        
        return metrics
    
    def list_available_models(self) -> List[str]:
        """List all available trained models."""
        if not os.path.exists(self.models_dir):
            return []
        
        models = []
        for filename in os.listdir(self.models_dir):
            if filename.endswith('.joblib'):
                model_name = filename.replace('.joblib', '')
                models.append(model_name)
        
        return models
