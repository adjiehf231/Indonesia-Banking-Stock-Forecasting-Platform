"""
Data Collection API Module.
"""
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import logging

from database.db_manager import DatabaseManager
from data.collect_data import (
    fetch_all_banks_data,
    fetch_stock_data,
    INDONESIAN_BANKS,
    TICKER_MAP
)
from data.indicators import calculate_all_indicators

logger = logging.getLogger(__name__)


class DataCollectionAPI:
    """API for collecting stock data from Yahoo Finance."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize the data collection API."""
        self.db_manager = db_manager
        
    def collect_all_banks(self, start_date: str = '2022-01-01') -> Dict[str, int]:
        """
        Collect data for all Indonesian banks.
        
        Args:
            start_date: Start date for data collection (YYYY-MM-DD)
            
        Returns:
            Dictionary with bank codes and number of records collected
        """
        results = {}
        
        for bank_code, bank_name in INDONESIAN_BANKS.items():
            logger.info(f"Collecting data for {bank_name} ({bank_code})...")
            
            try:
                df = fetch_stock_data(bank_code, start_date)
                
                if df.empty:
                    logger.warning(f"No data returned for {bank_code}")
                    results[bank_code] = 0
                    continue
                
                df = calculate_all_indicators(df)
                
                self.db_manager.insert_stock_data(df)
                
                self.db_manager.log_data_collection(
                    ticker=bank_code,
                    start_date=start_date,
                    end_date=datetime.now().strftime('%Y-%m-%d'),
                    records_count=len(df),
                    status='success'
                )
                
                results[bank_code] = len(df)
                logger.info(f"Successfully collected {len(df)} records for {bank_code}")
                
            except Exception as e:
                logger.error(f"Error collecting data for {bank_code}: {str(e)}")
                self.db_manager.log_data_collection(
                    ticker=bank_code,
                    start_date=start_date,
                    end_date=datetime.now().strftime('%Y-%m-%d'),
                    records_count=0,
                    status=f'failed: {str(e)}'
                )
                results[bank_code] = 0
        
        return results
    
    def collect_single_bank(self, ticker: str, start_date: str = '2022-01-01') -> int:
        """
        Collect data for a single bank.
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date for data collection
            
        Returns:
            Number of records collected
        """
        try:
            df = fetch_stock_data(ticker, start_date)
            
            if df.empty:
                return 0
            
            df = calculate_all_indicators(df)
            self.db_manager.insert_stock_data(df)
            
            return len(df)
            
        except Exception as e:
            logger.error(f"Error collecting data for {ticker}: {str(e)}")
            return 0
    
    def get_collection_status(self) -> pd.DataFrame:
        """Get the status of data collection."""
        return self.db_manager.get_collection_logs()
    
    def get_available_tickers(self) -> List[str]:
        """Get list of available stock tickers."""
        return self.db_manager.get_all_tickers()
    
    def get_bank_info(self) -> Dict[str, str]:
        """Get information about all banks."""
        return INDONESIAN_BANKS.copy()
