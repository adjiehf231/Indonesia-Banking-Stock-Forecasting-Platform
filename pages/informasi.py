"""
Informasi Page - Dataset info and metrics.
"""
import streamlit as st
import pandas as pd
import numpy as np


def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Check missing values in the dataframe."""
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    return pd.DataFrame({
        'Column': missing.index,
        'Missing Count': missing.values,
        'Missing %': missing_pct.values
    })


def check_duplicates(df: pd.DataFrame) -> dict:
    """Check for duplicate rows."""
    dup_count = df.duplicated().sum()
    return {
        'total_duplicates': dup_count,
        'duplicate_percentage': (dup_count / len(df)) * 100
    }


def check_outliers(df: pd.DataFrame, columns: list = None) -> dict:
    """Check for outliers using IQR method."""
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    outliers = {}
    for col in columns:
        if col in df.columns and df[col].dtype in [np.float64, np.int64]:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            if outlier_count > 0:
                outliers[col] = {
                    'count': outlier_count,
                    'percentage': (outlier_count / len(df)) * 100,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
    return outliers


def validate_range(df: pd.DataFrame) -> dict:
    """Validate if values are within expected ranges."""
    validation = {}
    
    # Price columns should be positive
    price_cols = ['open', 'high', 'low', 'close']
    for col in price_cols:
        if col in df.columns:
            negative_count = (df[col] <= 0).sum()
            if negative_count > 0:
                validation[col] = f"{negative_count} non-positive values found"
    
    # Volume should be non-negative
    if 'volume' in df.columns:
        negative_volume = (df['volume'] < 0).sum()
        if negative_volume > 0:
            validation['volume'] = f"{negative_volume} negative values found"
    
    # High should be >= Low
    if 'high' in df.columns and 'low' in df.columns:
        invalid_hl = (df['high'] < df['low']).sum()
        if invalid_hl > 0:
            validation['high_low'] = f"{invalid_hl} rows where High < Low"
    
    # Open, High, Low, Close relationship
    if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
        invalid_ohlc = ((df['high'] < df['open']) | (df['high'] < df['close']) |
                       (df['low'] > df['open']) | (df['low'] > df['close'])).sum()
        if invalid_ohlc > 0:
            validation['ohlc'] = f"{invalid_ohlc} rows with invalid OHLC relationship"
    
    return validation


def check_format_consistency(df: pd.DataFrame) -> dict:
    """Check data format consistency."""
    consistency = {}
    
    # Date format
    if 'date' in df.columns:
        try:
            pd.to_datetime(df['date'])
            consistency['date'] = "All dates are valid"
        except:
            consistency['date'] = "Some dates are invalid"
    
    # Numeric columns
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in numeric_cols:
        if col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                consistency[col] = "Numeric"
            else:
                consistency[col] = f"Non-numeric: {df[col].dtype}"
    
    return consistency


def check_data_distribution(df: pd.DataFrame) -> dict:
    """Check data distribution statistics."""
    numeric_cols = df.select_dtypes(include=[np.float64, np.int64]).columns
    distribution = {}
    
    for col in numeric_cols:
        if col in df.columns:
            distribution[col] = {
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'median': df[col].median(),
                'skewness': df[col].skew()
            }
    
    return distribution


def check_leakage(df: pd.DataFrame) -> dict:
    """Check for potential data leakage in features."""
    leakage = {}
    
    # Check if future information might be leaked
    # For example, if we have close and future_close columns
    future_cols = [col for col in df.columns if 'future' in col.lower()]
    if future_cols:
        leakage['future_columns'] = future_cols
    
    # Check if target is in features
    if 'target' in df.columns:
        leakage['target_in_features'] = "Target column present in features"
    
    return leakage


def check_scaling(df: pd.DataFrame) -> dict:
    """Check if data is scaled."""
    scaling_info = {}
    numeric_cols = df.select_dtypes(include=[np.float64, np.int64]).columns
    
    for col in numeric_cols:
        if col in df.columns and df[col].notna().sum() > 0:
            mean_val = df[col].mean()
            std_val = df[col].std()
            
            # If mean is around 0 and std is around 1, likely standardized
            if abs(mean_val) < 0.01 and abs(std_val - 1) < 0.01:
                scaling_info[col] = "Standardized (z-score)"
            # If min is around 0 and max is around 1, likely normalized
            elif df[col].min() >= 0 and df[col].max() <= 1:
                scaling_info[col] = "Normalized (0-1)"
            else:
                scaling_info[col] = "Not scaled"
    
    return scaling_info


def show_informasi():
    """Display the information page."""
    
    st.set_page_config(
        page_title="Informasi - Prediksi Saham Bank",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Informasi Dataset dan Model")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Info Dataset", 
        "Dataset Fix", 
        "Metrik Evaluasi",
        "Statistik"
    ])
    
    with tab1:
        st.header("Informasi Dataset Awal")
        
        try:
            from database.db_manager import DatabaseManager
            
            db = DatabaseManager()
            tickers = db.get_all_tickers()
            
            if tickers:
                selected_ticker = st.selectbox("Pilih Bank:", tickers)
                df = db.get_stock_data(selected_ticker)
                info = db.get_data_info(selected_ticker)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Records", f"{info['total_records']:,}")
                
                with col2:
                    start_date = info.get('start_date', 'N/A')
                    if start_date != 'N/A':
                        start_date = pd.to_datetime(start_date).strftime('%d %B %Y')
                    st.metric("Start Date", str(start_date))
                
                with col3:
                    end_date = info.get('end_date', 'N/A')
                    if end_date != 'N/A':
                        end_date = pd.to_datetime(end_date).strftime('%d %B %Y')
                    st.metric("End Date", str(end_date))
                
                # Data Quality Checks
                st.markdown("---")
                st.subheader("🔍 Pemeriksaan Kualitas Data")
                
                # Missing Values
                with st.expander("❌ Missing Value"):
                    if not df.empty:
                        missing_df = check_missing_values(df)
                        st.dataframe(missing_df, use_container_width=True)
                        total_missing = df.isnull().sum().sum()
                        if total_missing > 0:
                            st.warning(f"Total missing values: {total_missing}")
                        else:
                            st.success("✓ Tidak ada missing values!")
                    else:
                        st.info("Tidak ada data.")
                
                # Duplicates
                with st.expander("📑 Duplikat"):
                    if not df.empty:
                        dup_info = check_duplicates(df)
                        st.write(f"Total Duplikat: {dup_info['total_duplicates']}")
                        st.write(f"Persentase: {dup_info['duplicate_percentage']:.2f}%")
                        if dup_info['total_duplicates'] > 0:
                            st.warning("⚠️ Ada data duplikat!")
                        else:
                            st.success("✓ Tidak ada duplikat!")
                    else:
                        st.info("Tidak ada data.")
                
                # Outliers
                with st.expander("📊 Outlier"):
                    if not df.empty:
                        outliers = check_outliers(df)
                        if outliers:
                            st.warning(f"⚠️ Ditemukan outlier pada {len(outliers)} kolom:")
                            for col, info in outliers.items():
                                st.write(f"  - {col}: {info['count']} ({info['percentage']:.2f}%)")
                        else:
                            st.success("✓ Tidak ada outlier signifikan!")
                    else:
                        st.info("Tidak ada data.")
                
                # Range Validation
                with st.expander("✓ Validasi Range"):
                    if not df.empty:
                        validation = validate_range(df)
                        if validation:
                            st.warning("⚠️ Ditemukan issues:")
                            for col, msg in validation.items():
                                st.write(f"  - {col}: {msg}")
                        else:
                            st.success("✓ Semua nilai dalam range yang valid!")
                    else:
                        st.info("Tidak ada data.")
                
                # Format Consistency
                with st.expander("🔄 Konsistensi Format"):
                    if not df.empty:
                        consistency = check_format_consistency(df)
                        for col, status in consistency.items():
                            st.write(f"  - {col}: {status}")
                    else:
                        st.info("Tidak ada data.")
                
                # Distribution
                with st.expander("📈 Distribusi Data"):
                    if not df.empty:
                        distribution = check_data_distribution(df)
                        # Show histogram for key columns
                        key_cols = ['open', 'high', 'low', 'close', 'volume']
                        for col in key_cols:
                            if col in df.columns:
                                with st.expander(f"Distribusi {col}"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(f"Mean: {distribution[col]['mean']:.2f}")
                                        st.write(f"Std: {distribution[col]['std']:.2f}")
                                        st.write(f"Median: {distribution[col]['median']:.2f}")
                                    with col2:
                                        st.write(f"Min: {distribution[col]['min']:.2f}")
                                        st.write(f"Max: {distribution[col]['max']:.2f}")
                                        st.write(f"Skewness: {distribution[col]['skewness']:.2f}")
                    else:
                        st.info("Tidak ada data.")
                
                # Leakage
                with st.expander("⚠️ Leakage"):
                    if not df.empty:
                        leakage = check_leakage(df)
                        if leakage:
                            st.warning("⚠️ Potensi leakage detected:")
                            for col, msg in leakage.items():
                                st.write(f"  - {col}: {msg}")
                        else:
                            st.success("✓ Tidak ada leakage detected!")
                    else:
                        st.info("Tidak ada data.")
                
                # Scaling
                with st.expander("📏 Scaling/Normalization"):
                    if not df.empty:
                        scaling = check_scaling(df)
                        scaled_cols = [k for k, v in scaling.items() if v != "Not scaled"]
                        if scaled_cols:
                            st.info(f"Kolom yang discale: {', '.join(scaled_cols)}")
                        else:
                            st.info("Data belum di-scale/normalisasi")
                    else:
                        st.info("Tidak ada data.")
                        
            else:
                st.info("Belum ada data tersedia. Silakan collect data terlebih dahulu.")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab2:
        st.header("Data yang Telah Diproses")
        
        try:
            from api.preprocessing_api import PreprocessingAPI
            from database.db_manager import DatabaseManager
            
            db = DatabaseManager()
            preproc_api = PreprocessingAPI(db)
            tickers = db.get_all_tickers()
            
            if tickers:
                ticker = st.selectbox("Pilih Bank:", tickers, key="preproc_ticker")
                
                # Get raw data first
                df_raw = db.get_stock_data(ticker)
                
                if not df_raw.empty:
                    # Show preprocessing info
                    st.subheader(f"Data Preprocessing untuk {ticker}")
                    
                    # Check if preprocessing is available
                    if ticker in preproc_api.preprocessing_cache:
                        df_processed = preproc_api.get_cached_data(ticker)
                    else:
                        # Try to preprocess
                        try:
                            df_processed, _ = preproc_api.preprocess_data(ticker)
                        except Exception as e:
                            st.warning(f"Preprocessing belum tersedia: {str(e)}")
                            df_processed = pd.DataFrame()
                        
                    if not df_processed.empty:
                        st.dataframe(df_processed.head(10))
                        st.write(f"Total baris setelah preprocessing: {len(df_processed)}")
                        
                        # Data Quality Checks after preprocessing
                        st.markdown("---")
                        st.subheader("🔍 Pemeriksaan Kualitas Data (Setelah Preprocessing)")
                        
                        # Missing Values
                        with st.expander("❌ Missing Value"):
                            missing_df = check_missing_values(df_processed)
                            st.dataframe(missing_df, use_container_width=True)
                            total_missing = df_processed.isnull().sum().sum()
                            if total_missing > 0:
                                st.warning(f"Total missing values: {total_missing}")
                            else:
                                st.success("✓ Tidak ada missing values!")
                        
                        # Duplicates
                        with st.expander("📑 Duplikat"):
                            dup_info = check_duplicates(df_processed)
                            st.write(f"Total Duplikat: {dup_info['total_duplicates']}")
                            st.write(f"Persentase: {dup_info['duplicate_percentage']:.2f}%")
                            if dup_info['total_duplicates'] > 0:
                                st.warning("⚠️ Ada data duplikat!")
                            else:
                                st.success("✓ Tidak ada duplikat!")
                        
                        # Outliers
                        with st.expander("📊 Outlier"):
                            outliers = check_outliers(df_processed)
                            if outliers:
                                st.warning(f"⚠️ Ditemukan outlier pada {len(outliers)} kolom:")
                                for col, info in outliers.items():
                                    st.write(f"  - {col}: {info['count']} ({info['percentage']:.2f}%)")
                            else:
                                st.success("✓ Tidak ada outlier signifikan!")
                        
                        # Range Validation
                        with st.expander("✓ Validasi Range"):
                            validation = validate_range(df_processed)
                            if validation:
                                st.warning("⚠️ Ditemukan issues:")
                                for col, msg in validation.items():
                                    st.write(f"  - {col}: {msg}")
                            else:
                                st.success("✓ Semua nilai dalam range yang valid!")
                        
                        # Format Consistency
                        with st.expander("🔄 Konsistensi Format"):
                            consistency = check_format_consistency(df_processed)
                            for col, status in consistency.items():
                                st.write(f"  - {col}: {status}")
                        
                        # Distribution
                        with st.expander("📈 Distribusi Data"):
                            distribution = check_data_distribution(df_processed)
                            key_cols = ['open', 'high', 'low', 'close', 'volume']
                            for col in key_cols:
                                if col in df_processed.columns:
                                    with st.expander(f"Distribusi {col}"):
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.write(f"Mean: {distribution[col]['mean']:.2f}")
                                            st.write(f"Std: {distribution[col]['std']:.2f}")
                                            st.write(f"Median: {distribution[col]['median']:.2f}")
                                        with col2:
                                            st.write(f"Min: {distribution[col]['min']:.2f}")
                                            st.write(f"Max: {distribution[col]['max']:.2f}")
                                            st.write(f"Skewness: {distribution[col]['skewness']:.2f}")
                        
                        # Leakage
                        with st.expander("⚠️ Leakage"):
                            leakage = check_leakage(df_processed)
                            if leakage:
                                st.warning("⚠️ Potensi leakage detected:")
                                for col, msg in leakage.items():
                                    st.write(f"  - {col}: {msg}")
                            else:
                                st.success("✓ Tidak ada leakage detected!")
                        
                        # Scaling
                        with st.expander("📏 Scaling/Normalization"):
                            scaling = check_scaling(df_processed)
                            scaled_cols = [k for k, v in scaling.items() if v != "Not scaled"]
                            if scaled_cols:
                                st.info(f"Kolom yang discale: {', '.join(scaled_cols)}")
                            else:
                                st.info("Data belum di-scale/normalisasi")
                    else:
                        st.info("Silakan jalankan preprocessing terlebih dahulu.")
                else:
                    st.info("Tidak ada data untuk bank ini.")
            else:
                st.info("Tidak ada data tersedia.")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab3:
        st.header("Metrik Evaluasi Model")
        
        try:
            from database.db_manager import DatabaseManager
            
            db = DatabaseManager()
            metrics = db.get_model_metrics()
            
            if not metrics.empty:
                st.dataframe(metrics)
                
                # Show metrics summary
                st.subheader("Ringkasan Performa Model")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_mse = metrics['mse'].mean()
                    st.metric("Avg MSE", f"{avg_mse:.4f}" if pd.notna(avg_mse) else "N/A")
                
                with col2:
                    avg_rmse = metrics['rmse'].mean()
                    st.metric("Avg RMSE", f"{avg_rmse:.4f}" if pd.notna(avg_rmse) else "N/A")
                
                with col3:
                    avg_mae = metrics['mae'].mean()
                    st.metric("Avg MAE", f"{avg_mae:.4f}" if pd.notna(avg_mae) else "N/A")
                
                with col4:
                    avg_r2 = metrics['r2_score'].mean()
                    st.metric("Avg R²", f"{avg_r2:.4f}" if pd.notna(avg_r2) else "N/A")
            else:
                st.info("Belum ada model yang dilatih.")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab4:
        st.header("Statistik Deskriptif")
        
        try:
            from database.db_manager import DatabaseManager
            
            db = DatabaseManager()
            tickers = db.get_all_tickers()
            
            if tickers:
                ticker = st.selectbox("Pilih Bank:", tickers, key="stat_ticker")
                df = db.get_stock_data(ticker)
                
                if not df.empty:
                    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                    st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                    
                    # Show data sample
                    st.subheader("Sample Data")
                    st.dataframe(df.head(10))
            else:
                st.info("Tidak ada data tersedia.")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    show_informasi()
