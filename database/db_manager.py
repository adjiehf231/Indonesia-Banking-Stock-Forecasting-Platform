"""
Database Manager for SQLite operations.
"""
import sqlite3
import pandas as pd
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Tuple
import os


class DatabaseManager:
    """Manages SQLite database operations for stock price prediction."""
    
    def __init__(self, db_path: str = "stock_prediction.db"):
        self.db_path = db_path
        
    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        return conn
    
    def initialize_database(self) -> None:
        from database.schema import ALL_TABLES
        conn = self.get_connection()
        cursor = conn.cursor()
        for table_schema in ALL_TABLES:
            cursor.execute(table_schema)
        conn.commit()
        conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def execute_update(self, query: str, params: tuple = ()) -> None:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
    
    def _convert_value(self, val, col_name):
        """Convert value to appropriate format for SQLite."""
        if pd.isna(val):
            return None
        if col_name == 'date':
            if isinstance(val, (pd.Timestamp, datetime)):
                return pd.to_datetime(val).strftime('%Y-%m-%d')
            elif isinstance(val, str):
                return val
            return str(val)
        elif isinstance(val, (pd.Timestamp, datetime)):
            return pd.to_datetime(val).strftime('%Y-%m-%d')
        return val
    
    def insert_stock_data(self, data: pd.DataFrame) -> None:
        conn = self.get_connection()
        
        db_columns = [
            'ticker', 'date', 'open', 'high', 'low', 'close', 'volume',
            'ma_5', 'ma_10', 'ma_20', 'ma_50', 'ma_200',
            'ema_12', 'ema_26', 'macd', 'macd_signal', 'macd_hist',
            'vwap', 'rsi', 'stochastic_k', 'stochastic_d', 'roc',
            'bb_upper', 'bb_middle', 'bb_lower', 'atr', 'volatility'
        ]
        
        for _, row in data.iterrows():
            query = f"""
            INSERT OR REPLACE INTO stocks_data (
                {', '.join(db_columns)}
            ) VALUES ({', '.join(['?'] * len(db_columns))})
            """
            
            params = tuple(self._convert_value(row.get(col), col) for col in db_columns)
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def get_stock_data(self, ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        query = "SELECT * FROM stocks_data WHERE ticker = ?"
        params = (ticker,)
        
        if start_date:
            query += " AND date >= ?"
            params += (start_date,)
        if end_date:
            query += " AND date <= ?"
            params += (end_date,)
        
        query += " ORDER BY date ASC"
        
        conn = self.get_connection()
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_all_tickers(self) -> List[str]:
        query = "SELECT DISTINCT ticker FROM stocks_data ORDER BY ticker"
        results = self.execute_query(query)
        return [r[0] for r in results]
    
    def insert_model_metrics(self, ticker: str, model_name: str, metrics: Dict[str, float]) -> None:
        query = """
        INSERT OR REPLACE INTO model_metrics (
            ticker, model_name, mse, rmse, mae, r2_score, training_date
        ) VALUES (?, ?, ?, ?, ?, ?, date('now'))
        """
        params = (
            ticker, model_name,
            metrics.get('mse'), metrics.get('rmse'),
            metrics.get('mae'), metrics.get('r2_score')
        )
        self.execute_update(query, params)
    
    def get_model_metrics(self, ticker: str = None, model_name: str = None) -> pd.DataFrame:
        query = "SELECT * FROM model_metrics WHERE 1=1"
        params = []
        
        if ticker:
            query += " AND ticker = ?"
            params.append(ticker)
        if model_name:
            query += " AND model_name = ?"
            params.append(model_name)
        
        query += " ORDER BY training_date DESC"
        
        conn = self.get_connection()
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def insert_prediction(self, ticker: str, prediction_date: str, target_date: str,
                          predicted_price: float, model_name: str) -> None:
        query = """
        INSERT INTO predictions (
            ticker, prediction_date, target_date, predicted_price, model_name
        ) VALUES (?, ?, ?, ?, ?)
        """
        params = (ticker, prediction_date, target_date, predicted_price, model_name)
        self.execute_update(query, params)
    
    def get_predictions(self, ticker: str = None) -> pd.DataFrame:
        query = "SELECT * FROM predictions WHERE 1=1"
        params = []
        
        if ticker:
            query += " AND ticker = ?"
            params.append(ticker)
        
        query += " ORDER BY prediction_date DESC, target_date ASC"
        
        conn = self.get_connection()
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_data_info(self, ticker: str = None) -> Dict[str, Any]:
        conn = self.get_connection()
        
        if ticker:
            total_query = "SELECT COUNT(*) FROM stocks_data WHERE ticker = ?"
            total = self.execute_query(total_query, (ticker,))[0][0]
            date_query = "SELECT MIN(date), MAX(date) FROM stocks_data WHERE ticker = ?"
            date_range = self.execute_query(date_query, (ticker,))[0]
        else:
            total_query = "SELECT COUNT(*) FROM stocks_data"
            total = self.execute_query(total_query)[0][0]
            date_query = "SELECT MIN(date), MAX(date) FROM stocks_data"
            date_range = self.execute_query(date_query)[0]
        
        conn.close()
        
        return {
            'total_records': total,
            'start_date': date_range[0],
            'end_date': date_range[1],
            'tickers_count': len(self.get_all_tickers())
        }
    
    def log_data_collection(self, ticker: str, start_date: str, end_date: str,
                           records_count: int, status: str) -> None:
        query = """
        INSERT INTO data_collection_log (
            ticker, start_date, end_date, records_count, status
        ) VALUES (?, ?, ?, ?, ?)
        """
        params = (ticker, start_date, end_date, records_count, status)
        self.execute_update(query, params)
    
    def get_collection_logs(self) -> pd.DataFrame:
        query = "SELECT * FROM data_collection_log ORDER BY collected_at DESC"
        conn = self.get_connection()
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def update_best_model(self, ticker: str, best_model_name: str, metrics: Dict[str, float]) -> None:
        """Update the best model for a ticker."""
        query = """
        INSERT OR REPLACE INTO best_models (
            ticker, best_model_name, mse, rmse, mae, r2_score, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """
        params = (
            ticker, best_model_name,
            metrics.get('mse'), metrics.get('rmse'),
            metrics.get('mae'), metrics.get('r2_score')
        )
        self.execute_update(query, params)
    
    def get_best_model(self, ticker: str = None) -> pd.DataFrame:
        """Get the best model(s) for ticker(s)."""
        query = "SELECT * FROM best_models WHERE 1=1"
        params = []
        
        if ticker:
            query += " AND ticker = ?"
            params.append(ticker)
        
        query += " ORDER BY r2_score DESC"
        
        conn = self.get_connection()
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_best_model_name(self, ticker: str) -> str:
        """Get the name of the best model for a ticker."""
        query = "SELECT best_model_name FROM best_models WHERE ticker = ?"
        results = self.execute_query(query, (ticker,))
        if results:
            return results[0][0]
        return None
