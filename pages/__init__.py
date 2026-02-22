"""
Pages Package for Stock Prediction Application.

This package contains Streamlit page modules for the web interface.
"""

from .beranda import show_beranda
from .informasi import show_informasi
from .grafik import show_grafik
from .prediksi import show_prediksi

__all__ = [
    'show_beranda',
    'show_informasi',
    'show_grafik',
    'show_prediksi',
]
