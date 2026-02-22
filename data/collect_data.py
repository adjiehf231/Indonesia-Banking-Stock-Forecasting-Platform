"""
Data Collection Module - Fetches stock data from Yahoo Finance.
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Bank ticker symbols for Indonesian banks
INDONESIAN_BANKS = {
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

# Yahoo Finance ticker symbols (add .JK for Indonesia)
TICKER_MAP = {code: f"{code}.JK" for code in INDONESIAN_BANKS.keys()}


def fetch_stock_data(ticker: str, start_date: str = '2022-01-01', 
                     end_date: str = None, interval: str = '1d') -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'BMRI' or 'BMRI.JK')
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format (defaults to today)
        interval: Data interval ('1d', '1wk', '1mo', etc.)
    
    Returns:
        DataFrame with OHLCV data
    
    Raises:
        Exception: If data fetch fails
    """
    if not ticker.endswith('.JK'):
        ticker = f"{ticker}.JK"
    
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
    
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date, interval=interval)
        
        if df.empty:
            logger.warning(f"No data returned for {ticker}")
            return pd.DataFrame()
        
        # Reset index to make date a column
        df = df.reset_index()
        
        # Rename columns to lowercase
        df.columns = [col.lower() if col != 'Date' else 'date' for col in df.columns]
        
        # Drop unnecessary columns that cause database insert issues
        cols_to_drop = [col for col in ['dividends', 'stock splits'] if col in df.columns]
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)
        
        # Add ticker symbol without .JK
        df['ticker'] = ticker.replace('.JK', '')
        
        logger.info(f"Fetched {len(df)} records for {ticker}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {str(e)}")
        raise


def fetch_all_banks_data(start_date: str = '2022-01-01', 
                         end_date: str = None) -> Dict[str, pd.DataFrame]:
    """
    Fetch data for all Indonesian banks.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dictionary mapping bank code to DataFrame
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    all_data = {}
    
    for bank_code, bank_name in INDONESIAN_BANKS.items():
        logger.info(f"Fetching data for {bank_name} ({bank_code})...")
        
        try:
            df = fetch_stock_data(bank_code, start_date, end_date)
            
            if not df.empty:
                all_data[bank_code] = df
            else:
                logger.warning(f"No data available for {bank_code}")
            
            # Rate limiting to avoid API throttling
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Failed to fetch data for {bank_code}: {str(e)}")
            continue
    
    return all_data


def fetch_and_save_all_banks(db_manager, start_date: str = '2022-01-01') -> Dict[str, int]:
    """
    Fetch data for all banks and save to database.
    
    Args:
        db_manager: DatabaseManager instance
        start_date: Start date for data collection
    
    Returns:
        Dictionary with bank codes and number of records saved
    """
    from data.indicators import calculate_all_indicators
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    results = {}
    
    for bank_code in INDONESIAN_BANKS.keys():
        logger.info(f"Processing {bank_code}...")
        
        try:
            # Fetch raw data
            df = fetch_stock_data(bank_code, start_date, end_date)
            
            if df.empty:
                logger.warning(f"No data for {bank_code}, skipping...")
                results[bank_code] = 0
                continue
            
            # Calculate technical indicators
            df = calculate_all_indicators(df)
            
            # Save to database
            db_manager.insert_stock_data(df)
            
            # Log collection
            db_manager.log_data_collection(
                ticker=bank_code,
                start_date=start_date,
                end_date=end_date,
                records_count=len(df),
                status='success'
            )
            
            results[bank_code] = len(df)
            logger.info(f"Successfully saved {len(df)} records for {bank_code}")
            
        except Exception as e:
            logger.error(f"Error processing {bank_code}: {str(e)}")
            db_manager.log_data_collection(
                ticker=bank_code,
                start_date=start_date,
                end_date=end_date,
                records_count=0,
                status=f'failed: {str(e)}'
            )
            results[bank_code] = 0
        
        # Rate limiting
        time.sleep(1)
    
    return results


def get_latest_price(ticker: str) -> Optional[Dict]:
    """
    Get the latest price for a ticker.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Dictionary with price information or None if unavailable
    """
    try:
        if not ticker.endswith('.JK'):
            ticker = f"{ticker}.JK"
        
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            'current_price': info.get('currentPrice') or info.get('regularMarketPrice'),
            'open': info.get('open'),
            'high': info.get('dayHigh'),
            'low': info.get('dayLow'),
            'volume': info.get('volume'),
            'market_cap': info.get('marketCap'),
            'name': info.get('shortName') or info.get('longName')
        }
        
    except Exception as e:
        logger.error(f"Error fetching latest price for {ticker}: {str(e)}")
        return None


def check_data_update_needed(db_manager, ticker: str) -> bool:
    """
    Check if data update is needed for a ticker.
    
    Args:
        db_manager: DatabaseManager instance
        ticker: Stock ticker symbol
    
    Returns:
        True if update is needed, False otherwise
    """
    try:
        data = db_manager.get_stock_data(ticker)
        
        if data.empty:
            return True
        
        last_date = pd.to_datetime(data['date']).max()
        today = datetime.now().date()
        
        # Update if last data is older than yesterday
        return (today - last_date.date()).days > 0
        
    except Exception:
        return True
