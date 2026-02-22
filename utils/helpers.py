"""
Helper Functions Module.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def format_currency(value: float) -> str:
    """Format value as Indonesian Rupiah."""
    return f"Rp {value:,.0f}"


def format_percentage(value: float) -> str:
    """Format value as percentage."""
    return f"{value:.2f}%"


def get_period_days(period: str) -> int:
    """Convert period string to number of days."""
    period_map = {
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
    return period_map.get(period, 1)


def calculate_change(current: float, previous: float) -> tuple:
    """Calculate change amount and percentage."""
    change = current - previous
    change_pct = (change / previous) * 100 if previous != 0 else 0
    return change, change_pct


def get_bank_name(ticker: str) -> str:
    """Get full bank name from ticker."""
    bank_names = {
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
    return bank_names.get(ticker, ticker)


def get_ticker_list() -> list:
    """Get list of all ticker symbols."""
    return ['BMRI', 'BBRI', 'BBCA', 'BBNI', 'BBTN', 'BRIS', 'BNGA', 'NISP', 'BNLI', 'BDMN']


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime object."""
    try:
        return pd.to_datetime(date_str)
    except:
        return None


def format_date(date_obj: datetime, format_str: str = '%Y-%m-%d') -> str:
    """Format datetime object to string."""
    try:
        return date_obj.strftime(format_str)
    except:
        return str(date_obj)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    try:
        return numerator / denominator if denominator != 0 else default
    except:
        return default


def calculate_returns(prices: pd.Series) -> pd.Series:
    """Calculate returns from price series."""
    return prices.pct_change()


def calculate_cumulative_returns(returns: pd.Series) -> pd.Series:
    """Calculate cumulative returns from returns series."""
    return (1 + returns).cumprod() - 1
