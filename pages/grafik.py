"""Grafik (Charts) Page - Stock price visualization."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def show_grafik():
    """Display the charts page."""
    
    st.set_page_config(
        page_title="Grafik Harga Saham",
        page_icon="📈",
        layout="wide"
    )
    
    st.title("📈 Grafik Harga Saham 10 Bank Indonesia")
    
    try:
        from database.db_manager import DatabaseManager
        
        db = DatabaseManager()
        tickers = db.get_all_tickers()
        
        if not tickers:
            st.info("Belum ada data tersedia. Silakan collect data terlebih dahulu.")
            return
        
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
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            selected_ticker = st.selectbox("Pilih Bank:", tickers)
            bank_name = bank_names.get(selected_ticker, selected_ticker)
            st.write(f"**{bank_name}** ({selected_ticker})")
            
            df = db.get_stock_data(selected_ticker)
            
            if df.empty:
                st.warning("Tidak ada data untuk bank ini.")
                return
            
            date_range = st.date_input(
                "Pilih Tanggal:",
                value=(
                    pd.to_datetime(df['date'].min()).date(),
                    pd.to_datetime(df['date'].max()).date()
                ),
                min_value=pd.to_datetime(df['date'].min()).date(),
                max_value=pd.to_datetime(df['date'].max()).date()
            )
        
        with col2:
            chart_type = st.radio(
                "Jenis Grafik:",
                ["Candlestick", "Line"],
                horizontal=True
            )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df_filtered = df[
                (pd.to_datetime(df['date']).dt.date >= start_date) &
                (pd.to_datetime(df['date']).dt.date <= end_date)
            ].copy()
        else:
            df_filtered = df.copy()
        
        if df_filtered.empty:
            st.warning("Tidak ada data untuk rentang tanggal yang dipilih.")
            return
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Harga Saham', 'Volume'),
            row_heights=[0.7, 0.3]
        )
        
        if chart_type == "Candlestick":
            fig.add_trace(
                go.Candlestick(
                    x=df_filtered['date'],
                    open=df_filtered['open'],
                    high=df_filtered['high'],
                    low=df_filtered['low'],
                    close=df_filtered['close'],
                    name='Harga'
                ),
                row=1, col=1
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=df_filtered['date'],
                    y=df_filtered['close'],
                    mode='lines',
                    name='Close',
                    line=dict(color='blue', width=2)
                ),
                row=1, col=1
            )
        
        fig.add_trace(
            go.Bar(
                x=df_filtered['date'],
                y=df_filtered['volume'],
                name='Volume',
                marker_color='rgba(100, 100, 100, 0.5)'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title=f"Grafik Harga Saham {bank_name}",
            xaxis_rangeslider_visible=False,
            height=700,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📊 Statistik Harga")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Open Terakhir", f"Rp {df_filtered['open'].iloc[-1]:,.0f}")
        with col2:
            st.metric("High Terakhir", f"Rp {df_filtered['high'].iloc[-1]:,.0f}")
        with col3:
            st.metric("Low Terakhir", f"Rp {df_filtered['low'].iloc[-1]:,.0f}")
        with col4:
            st.metric("Close Terakhir", f"Rp {df_filtered['close'].iloc[-1]:,.0f}")
        with col5:
            st.metric("Volume Terakhir", f"{df_filtered['volume'].iloc[-1]:,.0f}")
        
        st.subheader("📈 Indikator Teknikal")
        
        indicators = st.multiselect(
            "Pilih Indikator:",
            ['ma_5', 'ma_10', 'ma_20', 'ma_50', 'rsi', 'macd'],
            default=['ma_20']
        )
        
        if indicators:
            fig_indicators = go.Figure()
            
            fig_indicators.add_trace(
                go.Scatter(
                    x=df_filtered['date'],
                    y=df_filtered['close'],
                    mode='lines',
                    name='Close',
                    line=dict(color='black', width=1)
                )
            )
            
            colors = {'ma_5': 'blue', 'ma_10': 'orange', 'ma_20': 'green', 'ma_50': 'red'}
            
            for ind in indicators:
                if ind in df_filtered.columns:
                    fig_indicators.add_trace(
                        go.Scatter(
                            x=df_filtered['date'],
                            y=df_filtered[ind],
                            mode='lines',
                            name=ind.upper(),
                            line=dict(color=colors.get(ind, 'gray'), width=1)
                        )
                    )
            
            fig_indicators.update_layout(
                title="Indikator Teknikal",
                xaxis_title="Tanggal",
                yaxis_title="Harga",
                height=400
            )
            
            st.plotly_chart(fig_indicators, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    show_grafik()
