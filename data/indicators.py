"""
Technical Indicators Calculation Module.
"""
import pandas as pd
import numpy as np


def calculate_sma(data: pd.DataFrame, periods: list = [5, 10, 20, 50, 200]) -> pd.DataFrame:
    """
    Calculate Simple Moving Averages.
    
    Args:
        data: DataFrame with 'close' column
        periods: List of periods for SMA calculation
    
    Returns:
        DataFrame with SMA columns added
    """
    df = data.copy()
    
    for period in periods:
        df[f'ma_{period}'] = df['close'].rolling(window=period).mean()
    
    return df


def calculate_ema(data: pd.DataFrame, periods: list = [12, 26]) -> pd.DataFrame:
    """
    Calculate Exponential Moving Averages.
    
    Args:
        data: DataFrame with 'close' column
        periods: List of periods for EMA calculation
    
    Returns:
        DataFrame with EMA columns added
    """
    df = data.copy()
    
    for period in periods:
        df[f'ema_{period}'] = df['close'].ewm(span=period, adjust=False).mean()
    
    return df


def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, 
                   signal: int = 9) -> pd.DataFrame:
    """
    Calculate MACD (Moving Average Convergence Divergence).
    
    Args:
        data: DataFrame with 'close' column
        fast: Fast EMA period
        slow: Slow EMA period
        signal: Signal line period
    
    Returns:
        DataFrame with MACD columns added
    """
    df = data.copy()
    
    # Calculate MACD line
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
    df['macd'] = ema_fast - ema_slow
    
    # Calculate Signal line
    df['macd_signal'] = df['macd'].ewm(span=signal, adjust=False).mean()
    
    # Calculate Histogram
    df['macd_hist'] = df['macd'] - df['macd_signal']
    
    return df


def calculate_vwap(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Volume Weighted Average Price (VWAP).
    
    Args:
        data: DataFrame with 'high', 'low', 'close', 'volume' columns
    
    Returns:
        DataFrame with VWAP column added
    """
    df = data.copy()
    
    # Typical Price
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    
    # Cumulative typical price * volume
    cumulative_tp_vol = (typical_price * df['volume']).cumsum()
    
    # Cumulative volume
    cumulative_vol = df['volume'].cumsum()
    
    # VWAP
    df['vwap'] = cumulative_tp_vol / cumulative_vol
    
    return df


def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Calculate Relative Strength Index (RSI).
    
    Args:
        data: DataFrame with 'close' column
        period: RSI period
    
    Returns:
        DataFrame with RSI column added
    """
    df = data.copy()
    
    # Calculate price changes
    delta = df['close'].diff()
    
    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate average gain and loss
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    return df


def calculate_stochastic(data: pd.DataFrame, k_period: int = 14, 
                        d_period: int = 3) -> pd.DataFrame:
    """
    Calculate Stochastic Oscillator.
    
    Args:
        data: DataFrame with 'high', 'low', 'close' columns
        k_period: %K period
        d_period: %D period
    
    Returns:
        DataFrame with Stochastic %K and %D columns added
    """
    df = data.copy()
    
    # Calculate %K
    lowest_low = df['low'].rolling(window=k_period).min()
    highest_high = df['high'].rolling(window=k_period).max()
    
    df['stochastic_k'] = 100 * ((df['close'] - lowest_low) / (highest_high - lowest_low))
    
    # Calculate %D (smoothed %K)
    df['stochastic_d'] = df['stochastic_k'].rolling(window=d_period).mean()
    
    return df


def calculate_roc(data: pd.DataFrame, period: int = 12) -> pd.DataFrame:
    """
    Calculate Rate of Change (ROC).
    
    Args:
        data: DataFrame with 'close' column
        period: ROC period
    
    Returns:
        DataFrame with ROC column added
    """
    df = data.copy()
    
    # ROC = ((Close - Close n periods ago) / Close n periods ago) * 100
    df['roc'] = ((df['close'] - df['close'].shift(period)) / 
                 df['close'].shift(period)) * 100
    
    return df


def calculate_bollinger_bands(data: pd.DataFrame, period: int = 20, 
                              std_dev: float = 2.0) -> pd.DataFrame:
    """
    Calculate Bollinger Bands.
    
    Args:
        data: DataFrame with 'close' column
        period: Moving average period
        std_dev: Number of standard deviations
    
    Returns:
        DataFrame with Bollinger Bands columns added
    """
    df = data.copy()
    
    # Middle Band (SMA)
    df['bb_middle'] = df['close'].rolling(window=period).mean()
    
    # Standard Deviation
    std = df['close'].rolling(window=period).std()
    
    # Upper and Lower Bands
    df['bb_upper'] = df['bb_middle'] + (std_dev * std)
    df['bb_lower'] = df['bb_middle'] - (std_dev * std)
    
    return df


def calculate_atr(data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Calculate Average True Range (ATR).
    
    Args:
        data: DataFrame with 'high', 'low', 'close' columns
        period: ATR period
    
    Returns:
        DataFrame with ATR column added
    """
    df = data.copy()
    
    # Calculate True Range components
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    
    # True Range is the max of the three
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    
    # ATR is the moving average of True Range
    df['atr'] = true_range.rolling(window=period).mean()
    
    return df


def calculate_historical_volatility(data: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """
    Calculate Historical Volatility.
    
    Args:
        data: DataFrame with 'close' column
        period: Period for volatility calculation
    
    Returns:
        DataFrame with volatility column added
    """
    df = data.copy()
    
    # Calculate log returns
    log_returns = np.log(df['close'] / df['close'].shift(1))
    
    # Historical volatility (annualized)
    df['volatility'] = log_returns.rolling(window=period).std() * np.sqrt(252) * 100
    
    return df


def calculate_all_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate all technical indicators.
    
    Args:
        data: DataFrame with OHLCV data
    
    Returns:
        DataFrame with all technical indicators added
    """
    df = data.copy()
    
    # Calculate all indicators
    df = calculate_sma(df)
    df = calculate_ema(df)
    df = calculate_macd(df)
    df = calculate_vwap(df)
    df = calculate_rsi(df)
    df = calculate_stochastic(df)
    df = calculate_roc(df)
    df = calculate_bollinger_bands(df)
    df = calculate_atr(df)
    df = calculate_historical_volatility(df)
    
    return df


def get_indicator_columns() -> list:
    """
    Get list of all technical indicator column names.
    
    Returns:
        List of indicator column names
    """
    return [
        'ma_5', 'ma_10', 'ma_20', 'ma_50', 'ma_200',
        'ema_12', 'ema_26',
        'macd', 'macd_signal', 'macd_hist',
        'vwap', 'rsi',
        'stochastic_k', 'stochastic_d',
        'roc', 'bb_upper', 'bb_middle', 'bb_lower',
        'atr', 'volatility'
    ]
