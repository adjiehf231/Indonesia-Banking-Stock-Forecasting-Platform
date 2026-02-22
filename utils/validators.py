"""
Validators Module - Data validation functions.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List


def validate_ticker(ticker: str) -> bool:
    """Validate stock ticker format."""
    valid_tickers = ['BMRI', 'BBRI', 'BBCA', 'BBNI', 'BBTN', 'BRIS', 'BNGA', 'NISP', 'BNLI', 'BDMN']
    return ticker.upper() in valid_tickers


def validate_date_range(start_date: str, end_date: str) -> bool:
    """Validate date range."""
    try:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        return start <= end
    except:
        return False


def validate_price_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate price data."""
    issues = []
    
    required_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            issues.append(f"Missing column: {col}")
    
    if 'high' in df.columns and 'low' in df.columns:
        if (df['high'] < df['low']).any():
            issues.append("High price is less than low price in some rows")
    
    for col in ['open', 'high', 'low', 'close']:
        if col in df.columns:
            if (df[col] <= 0).any():
                issues.append(f"{col} contains non-positive values")
    
    if 'volume' in df.columns:
        if (df['volume'] < 0).any():
            issues.append("Volume contains negative values")
    
    return {
        'is_valid': len(issues) == 0,
        'issues': issues
    }


def validate_model_metrics(metrics: Dict[str, float]) -> bool:
    """Validate model metrics."""
    required_metrics = ['mse', 'rmse', 'mae', 'r2_score']
    
    for metric in required_metrics:
        if metric not in metrics:
            return False
        if not isinstance(metrics[metric], (int, float)):
            return False
        if metrics[metric] < 0 and metric != 'r2_score':
            return False
    
    if 'r2_score' in metrics:
        if metrics['r2_score'] > 1 or metrics['r2_score'] < -1:
            return False
    
    return True


def validate_prediction_period(period: str) -> bool:
    """Validate prediction period."""
    valid_periods = ['1d', '3d', '1w', '2w', '1m', '3m', '6m', '9m', '1y', '2y']
    return period in valid_periods


def validate_feature_columns(df: pd.DataFrame) -> List[str]:
    """Validate and return missing feature columns."""
    required_features = [
        'open', 'high', 'low', 'close', 'volume',
        'ma_5', 'ma_10', 'ma_20', 'ma_50',
        'ema_12', 'ema_26',
        'macd', 'macd_signal',
        'vwap', 'rsi',
        'stochastic_k', 'stochastic_d',
        'roc', 'bb_upper', 'bb_middle', 'bb_lower',
        'atr', 'volatility'
    ]
    
    missing = []
    for col in required_features:
        if col not in df.columns:
            missing.append(col)
    
    return missing
