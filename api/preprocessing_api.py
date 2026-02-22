"""
Preprocessing API Module.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from database.db_manager import DatabaseManager
from data.preprocess import (
    handle_missing_values,
    remove_duplicates,
    handle_outliers,
    validate_range,
    check_data_leakage,
    normalize_data,
    preprocess_pipeline,
    get_preprocessing_report
)


class PreprocessingAPI:
    """API for data preprocessing operations."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize the preprocessing API."""
        self.db_manager = db_manager
        self.preprocessing_cache = {}
    
    def preprocess_data(self, ticker: str, remove_outliers: bool = True, 
                       normalize: bool = True) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Preprocess data for a given ticker.
        
        Args:
            ticker: Stock ticker symbol
            remove_outliers: Whether to remove outliers
            normalize: Whether to normalize data
            
        Returns:
            Tuple of (preprocessed DataFrame, preprocessing report)
        """
        df = self.db_manager.get_stock_data(ticker)
        
        if df.empty:
            return df, {'error': 'No data available'}
        
        original_df = df.copy()
        
        df_processed, scaler = preprocess_pipeline(
            df, 
            remove_outliers=remove_outliers,
            normalize=normalize
        )
        
        report = get_preprocessing_report(df_processed, original_df)
        
        self.preprocessing_cache[ticker] = {
            'data': df_processed,
            'report': report,
            'scaler': scaler
        }
        
        return df_processed, report
    
    def get_missing_value_info(self, ticker: str) -> pd.DataFrame:
        """Get information about missing values."""
        df = self.db_manager.get_stock_data(ticker)
        
        if df.empty:
            return pd.DataFrame()
        
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        
        result = pd.DataFrame({
            'column': missing.index,
            'missing_count': missing.values,
            'missing_percentage': missing_pct.values
        })
        
        return result[result['missing_count'] > 0].sort_values('missing_count', ascending=False)
    
    def get_duplicate_info(self, ticker: str) -> Dict[str, Any]:
        """Get information about duplicates."""
        df = self.db_manager.get_stock_data(ticker)
        
        if df.empty:
            return {'count': 0, 'percentage': 0}
        
        duplicates = df.duplicated().sum()
        
        return {
            'count': int(duplicates),
            'percentage': float((duplicates / len(df)) * 100)
        }
    
    def get_outlier_info(self, ticker: str) -> pd.DataFrame:
        """Get information about outliers."""
        df = self.db_manager.get_stock_data(ticker)
        
        if df.empty:
            return pd.DataFrame()
        
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        
        outliers_data = []
        
        for col in numeric_cols:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
                outlier_count = outlier_mask.sum()
                
                outliers_data.append({
                    'column': col,
                    'outlier_count': int(outlier_count),
                    'outlier_percentage': float((outlier_count / len(df)) * 100),
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound)
                })
        
        return pd.DataFrame(outliers_data)
    
    def get_range_validation(self, ticker: str) -> Dict[str, Any]:
        """Validate data ranges."""
        df = self.db_manager.get_stock_data(ticker)
        return validate_range(df)
    
    def get_leakage_check(self, ticker: str) -> Dict[str, Any]:
        """Check for potential data leakage."""
        df = self.db_manager.get_stock_data(ticker)
        return check_data_leakage(df)
    
    def get_full_preprocessing_report(self, ticker: str) -> Dict[str, Any]:
        """Generate a full preprocessing report."""
        return {
            'missing_values': self.get_missing_value_info(ticker).to_dict(),
            'duplicates': self.get_duplicate_info(ticker),
            'outliers': self.get_outlier_info(ticker).to_dict(),
            'range_validation': self.get_range_validation(ticker),
            'leakage_check': self.get_leakage_check(ticker)
        }
    
    def get_cached_data(self, ticker: str) -> pd.DataFrame:
        """Get cached preprocessed data."""
        if ticker in self.preprocessing_cache:
            return self.preprocessing_cache[ticker]['data']
        return None
