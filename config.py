"""
Configuration settings for the Stock Prediction Application.
"""

# Database settings
DB_PATH = "stock_prediction.db"

# Model settings
MODELS_DIR = "models"
RANDOM_STATE = 42
TEST_SIZE = 0.25

# Stock ticker settings
TICKERS = {
    'BMRI': 'Bank Mandiri',
    'BBRI': 'Bank Rakyat Indonesia',
    'BBCA': 'Bank Central Asia',
    'BBNI': 'Bank Negara Indonesia',
    'BBTN': 'Bank Tabungan Negara',
    'BRIS': 'Bank Syariah Indonesia',
    'BNGA': 'Bank CIMB Niaga',
    'NISP': 'Bank OCBC Indonesia',
    'BNLI': 'Bank Permata',
    'BDMN': 'Bank Danamon'
}

# Yahoo Finance ticker symbols (with .JK suffix for Indonesia)
YAHOO_TICKERS = {
    'BMRI': 'BMRI.JK',
    'BBRI': 'BBRI.JK',
    'BBCA': 'BBCA.JK',
    'BBNI': 'BBNI.JK',
    'BBTN': 'BBTN.JK',
    'BRIS': 'BRIS.JK',
    'BNGA': 'BNGA.JK',
    'NISP': 'NISP.JK',
    'BNLI': 'BNLI.JK',
    'BDMN': 'BDMN.JK'
}

# Data collection settings
START_DATE = "2022-01-01"
DATA_UPDATE_HOUR = 0  # 00:00 WIB
DATA_UPDATE_MINUTE = 0

# Technical indicator settings
INDICATOR_PERIODS = {
    'ma_5': 5,
    'ma_10': 10,
    'ma_20': 20,
    'ma_50': 50,
    'ma_200': 200,
    'ema_12': 12,
    'ema_26': 26,
    'rsi': 14,
    'stochastic_k': 14,
    'stochastic_d': 3,
    'roc': 12,
    'bollinger': 20,
    'atr': 14,
    'volatility': 20
}

# Prediction periods (in days)
PREDICTION_PERIODS = {
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

# Model types
MODEL_TYPES = [
    'random_forest',
    'xgboost',
    'lstm'
]

# Evaluation metrics
METRIC_NAMES = {
    'mse': 'Mean Squared Error',
    'rmse': 'Root Mean Squared Error',
    'mae': 'Mean Absolute Error',
    'r2_score': 'R² Score'
}

# Logging settings
LOG_DIR = "logs"
LOG_FILE = "app.log"
LOG_LEVEL = "INFO"

# Streamlit settings
PAGE_ICON = "📈"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"
