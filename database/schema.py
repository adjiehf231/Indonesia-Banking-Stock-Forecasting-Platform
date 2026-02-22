"""
Database schema definitions for stock price prediction project.
"""

# Stock data table schema
STOCKS_DATA_SCHEMA = """
CREATE TABLE IF NOT EXISTS stocks_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    date DATE NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    ma_5 REAL,
    ma_10 REAL,
    ma_20 REAL,
    ma_50 REAL,
    ma_200 REAL,
    ema_12 REAL,
    ema_26 REAL,
    macd REAL,
    macd_signal REAL,
    macd_hist REAL,
    vwap REAL,
    rsi REAL,
    stochastic_k REAL,
    stochastic_d REAL,
    roc REAL,
    bb_upper REAL,
    bb_middle REAL,
    bb_lower REAL,
    atr REAL,
    volatility REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ticker, date)
)
"""

# Model metrics table schema
MODEL_METRICS_SCHEMA = """
CREATE TABLE IF NOT EXISTS model_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    model_name TEXT NOT NULL,
    mse REAL,
    rmse REAL,
    mae REAL,
    r2_score REAL,
    training_date DATE DEFAULT (date('now')),
    UNIQUE(ticker, model_name, training_date)
)
"""

# Predictions table schema
PREDICTIONS_SCHEMA = """
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    prediction_date DATE NOT NULL,
    target_date DATE NOT NULL,
    predicted_price REAL,
    model_name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

# Data collection log table schema
DATA_COLLECTION_LOG_SCHEMA = """
CREATE TABLE IF NOT EXISTS data_collection_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    records_count INTEGER,
    status TEXT,
    collected_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

# Best model table schema
BEST_MODEL_SCHEMA = """
CREATE TABLE IF NOT EXISTS best_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL UNIQUE,
    best_model_name TEXT NOT NULL,
    mse REAL,
    rmse REAL,
    mae REAL,
    r2_score REAL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

# All tables list
ALL_TABLES = [
    STOCKS_DATA_SCHEMA,
    MODEL_METRICS_SCHEMA,
    PREDICTIONS_SCHEMA,
    DATA_COLLECTION_LOG_SCHEMA,
    BEST_MODEL_SCHEMA
]
