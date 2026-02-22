"""Prediksi (Prediction) Page - Stock price prediction."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def show_prediksi():
    """Display the prediction page."""
    
    st.set_page_config(
        page_title="Prediksi Harga Saham",
        page_icon="🔮",
        layout="wide"
    )
    
    st.title("🔮 Prediksi Harga Saham")
    
    st.warning("""
    **⚠️ DISCLAIMER:**
    
    Prediksi harga saham yang ditampilkan adalah hasil perhitungan matematis dan statistik.
    Ini bukan nasihat investasi. Hasil masa lalu tidak menjamin kinerja masa depan.
    Silakan konsultasikan dengan profesional keuangan sebelum membuat keputusan investasi.
    """)
    
    try:
        from database.db_manager import DatabaseManager
        
        db = DatabaseManager()
        tickers = db.get_all_tickers()
        
        if not tickers:
            st.info("Belum ada data tersedia. Silakan collect data terlebih dahulu.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_ticker = st.selectbox(
                "Pilih Bank:",
                tickers,
                index=0 if 'BMRI' in tickers else 0
            )
        
        with col2:
            selected_period = st.selectbox(
                "Pilih Periode Prediksi:",
                ["1d", "3d", "1w", "2w", "1m", "3m", "6m", "9m", "1y", "2y"],
                index=4
            )
        
        period_names = {
            "1d": "1 Hari",
            "3d": "3 Hari",
            "1w": "1 Minggu",
            "2w": "2 Minggu",
            "1m": "1 Bulan",
            "3m": "3 Bulan",
            "6m": "6 Bulan",
            "9m": "9 Bulan",
            "1y": "1 Tahun",
            "2y": "2 Tahun"
        }
        
        st.write(f"**Periode:** {period_names.get(selected_period, selected_period)}")
        
        if st.button("🔮 Prediksi", type="primary"):
            with st.spinner("Melakukan prediksi..."):
                try:
                    from api.predict_api import PredictionAPI
                    
                    predict_api = PredictionAPI(db)
                    
                    result = predict_api.get_prediction_by_period(
                        selected_ticker, 
                        selected_period
                    )
                    
                    if 'error' in result:
                        st.error(f"Error: {result['error']}")
                    else:
                        current_price = result.get('current_price', 0)
                        predicted_price = result.get('predicted_price', 0)
                        model_used = result.get('model_type', 'N/A')
                        predictions = result.get('predictions', [])
                        
                        if current_price > 0 and predicted_price > 0:
                            change = predicted_price - current_price
                            change_pct = (change / current_price) * 100
                            
                            st.subheader(f"Hasil Prediksi untuk {selected_ticker}")
                            st.info(f"**Model yang digunakan:** {model_used.upper()}")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric(
                                    "Harga Saat Ini",
                                    f"Rp {current_price:,.0f}"
                                )
                            
                            with col2:
                                st.metric(
                                    "Harga Prediksi",
                                    f"Rp {predicted_price:,.0f}",
                                    delta=f"{change:,.0f} ({change_pct:.2f}%)"
                                )
                            
                            with col3:
                                st.metric(
                                    "Perubahan",
                                    f"{'+' if change >= 0 else ''}{change_pct:.2f}%"
                                )
                            
                            # Create line chart for predictions
                            if predictions:
                                st.subheader("📈 Grafik Prediksi Harga Saham")
                                
                                # Prepare data for chart
                                dates = [p['target_date'] for p in predictions]
                                pred_prices = [p['predicted_price'] for p in predictions]
                                
                                # Get historical data for comparison
                                hist_data = db.get_stock_data(selected_ticker)
                                
                                # Get last 30 days of historical data
                                if not hist_data.empty:
                                    hist_data = hist_data.tail(30)
                                    # Handle date conversion safely
                                    if pd.api.types.is_datetime64_any_dtype(hist_data['date']):
                                        hist_dates = hist_data['date'].dt.strftime('%Y-%m-%d').tolist()
                                    else:
                                        hist_dates = pd.to_datetime(hist_data['date'], errors='coerce').dt.strftime('%Y-%m-%d').tolist()
                                    hist_prices = hist_data['close'].tolist()
                                
                                # Create the chart
                                fig = go.Figure()
                                
                                # Add historical price line
                                if not hist_data.empty:
                                    fig.add_trace(go.Scatter(
                                        x=hist_dates,
                                        y=hist_prices,
                                        mode='lines',
                                        name='Harga Historis',
                                        line=dict(color='blue', width=2)
                                    ))
                                
                                # Add predicted price line
                                fig.add_trace(go.Scatter(
                                    x=dates,
                                    y=pred_prices,
                                    mode='lines+markers',
                                    name='Prediksi',
                                    line=dict(color='red', width=2),
                                    marker=dict(size=6)
                                ))
                                
                                # Add current price marker
                                fig.add_trace(go.Scatter(
                                    x=[dates[0] if dates else None],
                                    y=[current_price],
                                    mode='markers',
                                    name='Harga Saat Ini',
                                    marker=dict(color='green', size=12, symbol='diamond')
                                ))
                                
                                fig.update_layout(
                                    title=f'Prediksi Harga Saham {selected_ticker}',
                                    xaxis_title='Tanggal',
                                    yaxis_title='Harga (Rp)',
                                    hovermode='x unified',
                                    legend=dict(
                                        yanchor="top",
                                        y=0.99,
                                        xanchor="left",
                                        x=0.01
                                    ),
                                    height=500
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Show prediction details in expandable section
                                with st.expander("📋 Detail Prediksi per Hari"):
                                    pred_df = pd.DataFrame(predictions)
                                    # Handle date formatting safely
                                    if 'target_date' in pred_df.columns:
                                        pred_df['target_date'] = pd.to_datetime(pred_df['target_date'], errors='coerce').dt.strftime('%d %B %Y')
                                    pred_df = pred_df[['target_date', 'predicted_price', 'ml_prediction', 'trend_prediction']]
                                    pred_df.columns = ['Tanggal', 'Harga Prediksi', 'ML Prediction', 'Trend Prediction']
                                    pred_df['Harga Prediksi'] = pred_df['Harga Prediksi'].apply(lambda x: f"Rp {x:,.0f}")
                                    pred_df['ML Prediction'] = pred_df['ML Prediction'].apply(lambda x: f"Rp {x:,.0f}" if pd.notna(x) else 'N/A')
                                    pred_df['Trend Prediction'] = pred_df['Trend Prediction'].apply(lambda x: f"Rp {x:,.0f}" if pd.notna(x) else 'N/A')
                                    st.dataframe(pred_df, use_container_width=True)
                            
                            st.success("Prediksi berhasil dibuat!")
                            
                except Exception as e:
                    st.error(f"Error saat melakukan prediksi: {str(e)}")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    show_prediksi()
