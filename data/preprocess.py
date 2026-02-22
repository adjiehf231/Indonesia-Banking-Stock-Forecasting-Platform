"""
Data Preprocessing Module.
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    
    Args:
        df: Input DataFrame
        strategy: Strategy to handle missing values ('drop', 'ffill', 'bfill', 'mean', 'median')
    
    Returns:
        DataFrame with missing values handled
    """
    df = df.copy()
    
    if strategy == 'drop':
        # Drop rows with any missing values
        df = df.dropna()
    elif strategy == 'ffill':
        # Forward fill
        df = df.fillna(method='ffill')
    elif strategy == 'bfill':
        # Backward fill
        df = df.fillna(method='bfill')
    elif strategy == 'mean':
        # Fill with mean of each column
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == 'median':
        # Fill with median of each column
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    return df


def remove_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    """
    Remove duplicate rows from the dataset.
    
    Args:
        df: Input DataFrame
        subset: Columns to consider for identifying duplicates
    
    Returns:
        DataFrame with duplicates removed
    """
    df = df.copy()
    initial_count = len(df)
    df = df.drop_duplicates(subset=subset, keep='first')
    removed_count = initial_count - len(df)
    
    if removed_count > 0:
        print(f"Removed {removed_count} duplicate rows")
    
    return df


def handle_outliers(df: pd.DataFrame, columns: list = None, 
                   method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
    """
    Handle outliers in the dataset.
    
    Args:
        df: Input DataFrame
        columns: Columns to check for outliers
        method: Method to handle outliers ('iqr', 'zscore')
        threshold: Threshold for outlier detection
    
    Returns:
        DataFrame with outliers handled
    """
    df = df.copy()
    
    if columns is None:
        # Only check numeric columns
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
        # Remove non-feature columns
        columns = [c for c in columns if c not in ['id', 'ticker', 'date']]
    
    if method == 'iqr':
        # IQR method
        for col in columns:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                # Cap outliers instead of removing
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
    
    elif method == 'zscore':
        # Z-score method
        for col in columns:
            if col in df.columns:
                mean = df[col].mean()
                std = df[col].std()
                if std > 0:
                    z_scores = np.abs((df[col] - mean) / std)
                    # Cap outliers
                    df.loc[z_scores > threshold, col] = mean + threshold * std
    
    return df


def validate_range(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate data ranges.
    
    Args:
        df: Input DataFrame
    
    Returns:
        Dictionary with validation results
    """
    issues = []
    
    # Check for negative prices
    price_cols = ['open', 'high', 'low', 'close']
    for col in price_cols:
        if col in df.columns:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                issues.append(f"{col}: {negative_count} negative values found")
    
    # Check for zero or negative volume
    if 'volume' in df.columns:
        zero_vol = (df['volume'] <= 0).sum()
        if zero_vol > 0:
            issues.append(f"volume: {zero_vol} zero or negative values found")
    
    # Check for high > low
    if all(col in df.columns for col in ['high', 'low']):
        invalid_hl = (df['high'] < df['low']).sum()
        if invalid_hl > 0:
            issues.append(f"high < low: {invalid_hl} invalid rows found")
    
    # Check for high >= open, close
    if 'high' in df.columns:
        if 'open' in df.columns:
            invalid_high = (df['high'] < df['open']).sum()
            if invalid_high > 0:
                issues.append(f"high < open: {invalid_high} invalid rows found")
        if 'close' in df.columns:
            invalid_high = (df['high'] < df['close']).sum()
            if invalid_high > 0:
                issues.append(f"high < close: {invalid_high} invalid rows found")
    
    return {
        'is_valid': len(issues) == 0,
        'issues': issues
    }


def check_data_leakage(df: pd.DataFrame, target_col: str = 'close') -> Dict[str, Any]:
    """
    Check for potential data leakage.
    
    Args:
        df: Input DataFrame
        target_col: Target column name
    
    Returns:
        Dictionary with leakage check results
    """
    issues = []
    
    # Check if future information is being used (look-ahead bias)
    # This is a simplified check - in practice, you'd check the data splitting
    
    # Check for highly correlated features
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in ['id', 'date']]
    
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        high_corr_pairs = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > 0.95:
                    high_corr_pairs.append(
                        (corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j])
                    )
        
        if high_corr_pairs:
            issues.append(f"Highly correlated features found: {len(high_corr_pairs)} pairs")
    
    return {
        'has_leakage': len(issues) > 0,
        'issues': issues
    }


def normalize_data(df: pd.DataFrame, columns: list = None, 
                  method: str = 'standard') -> Tuple[pd.DataFrame, Any]:
    """
    Normalize/scale the data.
    
    Args:
        df: Input DataFrame
        columns: Columns to normalize
        method: Normalization method ('standard', 'minmax')
    
    Returns:
        Tuple of (normalized DataFrame, scaler object)
    """
    df = df.copy()
    
    if columns is None:
        # Get all numeric columns except target
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
        columns = [c for c in columns if c not in ['id', 'ticker', 'date', 'close']]
    
    if method == 'standard':
        scaler = StandardScaler()
    else:
        scaler = MinMaxScaler()
    
    df[columns] = scaler.fit_transform(df[columns])
    
    return df, scaler


def get_data_info(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get comprehensive information about the dataset.
    
    Args:
        df: Input DataFrame
    
    Returns:
        Dictionary with data information
    """
    info = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicates': df.duplicated().sum(),
        'numeric_summary': df.describe().to_dict() if not df.empty else {}
    }
    
    return info


def preprocess_pipeline(df: pd.DataFrame, remove_outliers: bool = True,
                      normalize: bool = True) -> Tuple[pd.DataFrame, Any]:
    """
    Complete preprocessing pipeline.
    
    Args:
        df: Input DataFrame
        remove_outliers: Whether to remove outliers
        normalize: Whether to normalize data
    
    Returns:
        Tuple of (preprocessed DataFrame, scaler object)
    """
    scaler = None
    
    # Handle missing values
    df = handle_missing_values(df, strategy='drop')
    
    # Remove duplicates
    df = remove_duplicates(df, subset=['ticker', 'date'])
    
    # Handle outliers
    if remove_outliers:
        df = handle_outliers(df, method='iqr', threshold=1.5)
    
    # Normalize data
    if normalize:
        df, scaler = normalize_data(df, method='standard')
    
    return df, scaler


def get_preprocessing_report(df: pd.DataFrame, original_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Generate a comprehensive preprocessing report.
    
    Args:
        df: Preprocessed DataFrame
        original_df: Original DataFrame before preprocessing
    
    Returns:
        Dictionary with preprocessing report
    """
    report = {
        'shape_after': df.shape,
        'missing_values': df.isnull().sum().sum(),
        'duplicates': df.duplicated().sum()
    }
    
    if original_df is not None:
        report['shape_before'] = original_df.shape
        report['rows_removed'] = original_df.shape[0] - df.shape[0]
        report['columns_removed'] = original_df.shape[1] - df.shape[1]
    
    # Validation checks
    range_validation = validate_range(df)
    report['range_validation'] = range_validation
    
    # Leakage check
    leakage_check = check_data_leakage(df)
    report['leakage_check'] = leakage_check
    
    return report
