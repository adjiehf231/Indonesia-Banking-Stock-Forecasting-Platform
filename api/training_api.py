"""
Training API Module.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
import logging

from database.db_manager import DatabaseManager
from models.model_manager import ModelManager

logger = logging.getLogger(__name__)


class TrainingAPI:
    """API for model training operations."""
    
    def __init__(self, db_manager: DatabaseManager, models_dir: str = 'models'):
        """Initialize the training API."""
        self.db_manager = db_manager
        self.model_manager = ModelManager(models_dir)
    
    def train_model(self, ticker: str, model_type: str = 'all') -> Dict[str, Any]:
        """
        Train models for a given ticker.
        
        Args:
            ticker: Stock ticker symbol
            model_type: Type of model to train ('all', 'random_forest', 'xgboost', 'lstm')
            
        Returns:
            Dictionary with training results
        """
        df = self.db_manager.get_stock_data(ticker)
        
        if df.empty:
            return {'error': 'No data available for training'}
        
        results = {}
        
        if model_type == 'all':
            results = self.model_manager.train_all_models(df, ticker)
        else:
            try:
                model = self.model_manager.get_model(model_type)
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
                    raise ValueError(f"Insufficient data after cleaning: only {len(X_clean)} samples")
                
                metrics = model.train(X_clean, y_clean)
                results[model_type] = metrics
                
                key = f"{ticker}_{model_type}"
                self.model_manager.models[key] = model
                self.model_manager.save_model(model, ticker, model_type)
                
            except Exception as e:
                logger.error(f"Error training {model_type}: {str(e)}")
                results[model_type] = {'error': str(e)}
        
        for model_name, metrics in results.items():
            if 'error' not in metrics:
                self.db_manager.insert_model_metrics(ticker, model_name, metrics)
        
        # Auto-select and save best model after training
        self.select_and_save_best_model(ticker)
        
        return results
    
    def select_and_save_best_model(self, ticker: str) -> Dict[str, Any]:
        """
        Select the best model for a ticker based on R2 score and save to database.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with best model information
        """
        metrics = self.db_manager.get_model_metrics(ticker)
        
        if metrics.empty:
            return {'error': 'No metrics available'}
        
        # Find the best model based on R2 score
        best_idx = metrics['r2_score'].idxmax()
        best_model_name = metrics.loc[best_idx, 'model_name']
        best_metrics = {
            'mse': metrics.loc[best_idx, 'mse'],
            'rmse': metrics.loc[best_idx, 'rmse'],
            'mae': metrics.loc[best_idx, 'mae'],
            'r2_score': metrics.loc[best_idx, 'r2_score']
        }
        
        # Save to best_models table
        self.db_manager.update_best_model(ticker, best_model_name, best_metrics)
        
        return {
            'ticker': ticker,
            'best_model': best_model_name,
            'metrics': best_metrics
        }
    
    def train_all_tickers(self, model_type: str = 'all') -> Dict[str, Any]:
        """
        Train models for all available tickers.
        
        Args:
            model_type: Type of model to train
            
        Returns:
            Dictionary with training results for all tickers
        """
        tickers = self.db_manager.get_all_tickers()
        
        all_results = {}
        
        for ticker in tickers:
            logger.info(f"Training models for {ticker}...")
            try:
                results = self.train_model(ticker, model_type)
                all_results[ticker] = results
            except Exception as e:
                logger.error(f"Error training for {ticker}: {str(e)}")
                all_results[ticker] = {'error': str(e)}
        
        return all_results
    
    def get_model_metrics(self, ticker: str = None, model_name: str = None) -> pd.DataFrame:
        """Get model metrics from the database."""
        return self.db_manager.get_model_metrics(ticker, model_name)
    
    def get_best_model(self, ticker: str) -> str:
        """Get the best performing model for a ticker based on R2 score."""
        metrics = self.db_manager.get_model_metrics(ticker)
        
        if metrics.empty:
            return None
        
        best_idx = metrics['r2_score'].idxmax()
        return metrics.loc[best_idx, 'model_name']
    
    def list_available_models(self) -> List[str]:
        """List all available trained models."""
        return self.model_manager.list_available_models()
    
    def get_training_status(self) -> Dict[str, Any]:
        """Get training status information."""
        tickers = self.db_manager.get_all_tickers()
        available_models = self.list_available_models()
        
        return {
            'total_tickers': len(tickers),
            'available_tickers': tickers,
            'total_models': len(available_models),
            'available_models': available_models
        }
