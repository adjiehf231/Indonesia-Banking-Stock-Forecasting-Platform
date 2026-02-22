"""
Main Streamlit Application for Stock Price Prediction.
"""
import streamlit as st
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Prediksi Harga Saham 10 Bank Indonesia",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application entry point."""
    
    # Display Beranda content directly
    st.title("📈 Prediksi Harga Saham 10 Bank Terbesar di Indonesia")
    st.markdown("---")
    
    st.header("🎯 Tentang Proyek")
    st.write("""
    Proyek ini adalah aplikasi prediksi harga saham untuk 10 bank terbesar di Indonesia 
    menggunakan teknik Machine Learning dan Deep Learning. Aplikasi ini mengambil data 
    historis dari Yahoo Finance dan menghitung berbagai indikator teknis untuk membantu 
    memprediksi pergerakan harga saham di masa depan.
    """)
    
    st.header("⚠️ Disclaimer")
    st.warning("""
    **PERINGATAN PENTING:**
    
    - Prediksi harga saham yang ditampilkan dalam aplikasi ini **TIDAK** merupakan nasihat investasi
    - Historikal performa tidak menjamin hasil di masa depan
    - Trading dan investasi saham memiliki risiko tinggi
    - Gunakan aplikasi ini hanya sebagai bahan referensi
    - Konsultasikan dengan profesional keuangan sebelum membuat keputusan investasi
    - Penulis tidak bertanggung jawab atas kerugian finansial
    """)
    
    st.header("📊 Dataset")
    st.write("""
    Aplikasi ini menggunakan data historis saham dari tahun 2022 hingga sekarang, 
    dengan update data otomatis setiap hari pada pukul 00:00 WIB.
    
    **10 Bank yang Dipantau:**
    """)
    
    banks = [
        ("BMRI", "Bank Mandiri"),
        ("BBRI", "Bank Rakyat Indonesia"),
        ("BBCA", "Bank Central Asia"),
        ("BBNI", "Bank Negara Indonesia"),
        ("BBTN", "Bank Tabungan Negara"),
        ("BRIS", "Bank Syariah Indonesia"),
        ("BNGA", "Bank CIMB Niaga"),
        ("NISP", "Bank OCBC Indonesia"),
        ("BNLI", "Bank Permata"),
        ("BDMN", "Bank Danamon")
    ]
    
    for i, (code, name) in enumerate(banks, 1):
        st.write(f"{i}. **{code}** - {name}")
    
    st.header("🔧 Metode dan Model")
    st.write("""
    Aplikasi ini menggunakan beberapa model Machine Learning:
    
    1. **Random Forest** - Ensemble learning dengan decision trees
    2. **XGBoost** - Gradient boosting algorithm
    3. **LSTM** - Long Short-Term Memory neural network untuk time series
    
    **Fitur yang Digunakan (Technical Indicators):**
    - Moving Average (MA) - 5, 10, 20, 50, 200 hari
    - Exponential Moving Average (EMA) - 12, 26 hari
    - MACD (Moving Average Convergence Divergence)
    - VWAP (Volume Weighted Average Price)
    - RSI (Relative Strength Index)
    - Stochastic Oscillator
    - ROC (Rate of Change)
    - Bollinger Bands
    - ATR (Average True Range)
    - Historical Volatility
    """)
    
    st.header("🛠️ Tech Stack")
    st.write("""
    - **Streamlit** - Web framework untuk Python
    - **yfinance** - Pengambilan data saham dari Yahoo Finance
    - **Pandas & NumPy** - Manipulasi dan analisis data
    - **Scikit-learn** - Machine Learning
    - **XGBoost** - Gradient Boosting
    - **TensorFlow/Keras** - Deep Learning (LSTM)
    - **Joblib** - Penyimpanan model
    - **SQLite** - Database lokal
    """)
    
    st.header("👨‍💻 Kredit")
    st.write(f"""
    Dibuat dengan ❤️ menggunakan Python dan Streamlit
    
    **Versi:** 1.0.0
    **Terakhir Diupdate:** {datetime.now().strftime('%d %B %Y')}
    
    © 2026 Prediksi Harga Saham Bank Indonesia
    """)
    
    st.markdown("---")
    st.write("Silakan pilih menu di sidebar untuk melihat informasi lebih lanjut.")
    
    # Sidebar
    st.sidebar.markdown("### ℹ️ Informasi")
    st.sidebar.info(
        """
        **Prediksi Harga Saham**
        
        Aplikasi ini menyediakan prediksi harga 
        saham untuk 10 bank terbesar di Indonesia.
        
        Data diambil dari Yahoo Finance.
        
        ⚠️ Disclaimer: Ini bukan nasihat investasi.
        """
    )


if __name__ == "__main__":
    main()
