"""
Data Information API Module.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from database.db_manager import DatabaseManager


class DataInfoAPI:
    """API for getting data information and validation."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize the data info API."""
        self.db_manager = db_manager
    
    def get_data_info(self, ticker: str = None) -> Dict[str, Any]:
        """Get basic information about the data."""
        return self.db_manager.get_data_info(ticker)
    
    def check_missing_values(self, ticker: str = None) -> pd.DataFrame:
        """Check for missing values in the data."""
        if ticker:
            df = self.db_manager.get_stock_data(ticker)
        else:
            df = self.db_manager.get_stock_data('BMRI')
        
        if df.empty:
            return pd.DataFrame()
        
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        
        result = pd.DataFrame({
            'column': missing.index,
            'missing_count': missing.values,
            'missing_percentage': missing_pct.values
        })
        
        return result[result['missing_count'] > 0]
    
    def check_duplicates(self, ticker: str) -> int:
        """Check for duplicate rows."""
        df = self.db_manager.get_stock_data(ticker)
        if df.empty:
            return 0
        return df.duplicated().sum()
    
    def check_outliers(self, ticker: str, columns: List[str] = None) -> Dict[str, Any]:
        """Check for outliers using IQR method."""
        df = self.db_manager.get_stock_data(ticker)
        
        if df.empty:
            return {}
        
        if columns is None:
            columns = ['open', 'high', 'low', 'close', 'volume']
        
        outliers = {}
        
        for col in columns:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
                
                outliers[col] = {
                    'count': int(outlier_count),
                    'percentage': float((outlier_count / len(df)) * 100),
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound)
                }
        
        return outliers
    
    def validate_ranges(self, ticker: str) -> Dict[str, Any]:
        """Validate data ranges."""
        df = self.db_manager.get_stock_data(ticker)
        
        if df.empty:
            return {'is_valid': True, 'issues': []}
        
        issues = []
        
        price_cols = ['open', 'high', 'low', 'close']
        for col in price_cols:
            if col in df.columns:
                if (df[col] <= 0).any():
                    issues.append(f"{col} has non-positive values")
        
        if 'volume' in df.columns:
            if (df['volume'] < 0).any():
                issues.append("volume has negative values")
        
        if 'high' in df.columns and 'low' in df.columns:
            if (df['high'] < df['low']).any():
                issues.append("high is less than low in some rows")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues
        }
    
    def get_data_distribution(self, ticker: str, columns: List[str] = None) -> Dict[str, Any]:
        """Get data distribution statistics."""
        df = self.db_manager.get_stock_data(ticker)
        
        if df.empty:
            return {}
        
        if columns is None:
            columns = ['open', 'high', 'low', 'close', 'volume']
        
        distribution = {}
        
        for col in columns:
            if col in df.columns:
                distribution[col] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'q25': float(df[col].quantile(0.25)),
                    'q75': float(df[col].quantile(0.75))
                }
        
        return distribution
    
    def get_full_report(self, ticker: str) -> Dict[str, Any]:
        """Generate a full data report."""
        return {
            'basic_info': self.get_data_info(ticker),
            'missing_values': self.check_missing_values(ticker).to_dict(),
            'duplicates': self.check_duplicates(ticker),
            'outliers': self.check_outliers(ticker),
            'range_validation': self.validate_ranges(ticker),
            'distribution': self.get_data_distribution(ticker)
        }
