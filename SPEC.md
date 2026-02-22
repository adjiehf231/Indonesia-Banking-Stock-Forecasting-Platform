# Prediksi Harga Saham 10 Bank Terbesar di Indonesia

## Project Overview
- **Project Name**: Stock Price Prediction for 10 Biggest Indonesian Banks
- **Type**: Data Science Web Application
- **Core Functionality**: Real-time stock price prediction using technical indicators and machine learning models
- **Target Users**: Investors, traders, and data science enthusiasts interested in Indonesian banking stocks

## 10 Banks with Yahoo Finance Ticker Symbols
| No | Bank Name | Ticker Symbol |
|----|-----------|---------------|
| 1 | Bank Mandiri | BMRI.JK |
| 2 | Bank Rakyat Indonesia | BBRI.JK |
| 3 | Bank Central Asia | BBCA.JK |
| 4 | Bank Negara Indonesia | BBNI.JK |
| 5 | Bank Tabungan Negara | BBTN.JK |
| 6 | Bank Syariah Indonesia | BRIS.JK |
| 7 | Bank CIMB Niaga | BNGA.JK |
| 8 | Bank OCBC Indonesia | NISP.JK |
| 9 | Bank Permata | BNLI.JK |
| 10 | Bank Danamon | BDMN.JK |

## Features/Technical Indicators

### Price Data
- Open (harga pembukaan)
- High (harga tertinggi)
- Low (harga terendah)
- Close (harga penutupan)
- Volume (jumlah transaksi)

### Technical Indicators
1. **Moving Average (MA)** - Simple moving average at 5, 10, 20, 50, 200 periods
2. **Exponential Moving Average (EMA)** - EMA at 12, 26 periods
3. **MACD** - Moving Average Convergence Divergence (12, 26, 9)
4. **VWAP** - Volume Weighted Average Price
5. **RSI** - Relative Strength Index (14 periods)
6. **Stochastic Oscillator** - %K and %D (14, 3 periods)
7. **ROC** - Rate of Change (12 periods)
8. **Bollinger Bands** - Upper, Middle, Lower (20, 2)
9. **ATR** - Average True Range (14 periods)
10. **Historical Volatility** - 20 periods

## Tech Stack
- **Frontend**: Streamlit
- **Data Source**: yfinance (Yahoo Finance)
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, XGBoost, TensorFlow/Keras (LSTM)
- **Model Storage**: Joblib
- **Database**: SQLite

## API Specifications

### 1. Collect Data API
- **Endpoint**: Internal function (collect_data.py)
- **Schedule**: Run daily at 00:00 WIB
- **Data Range**: 2022-01-01 to current date
- **Storage**: SQLite database

### 2. Data Information API
- Check missing values
- Check duplicates
- Check outliers (using IQR method)
- Validate range (price > 0, volume >= 0)
- Check format consistency
- Check data distribution
- Check data leakage
- Scaling/Normalization (StandardScaler, MinMaxScaler)

### 3. Preprocessing Data API
- Same checks as Data Information API
- Display after preprocessing results
- Auto-run after collect data completes

### 4. Training Model API
- Auto-run after preprocessing completes
- Models: Random Forest, XGBoost, LSTM
- Features: All technical indicators
- Target: Close price

### 5. Evaluation & Validation API
- Metrics: MSE, RMSE, MAE, R² Score
- Auto-run after training completes
- Cross-validation with 5 folds

### 6. Prediction API
- Input: Stock ticker, prediction period
- Output: Predicted prices with confidence intervals
- Prediction periods: 1 day, 3 days, 1 week, 2 weeks, 1 month, 3 months, 6 months, 9 months, 1 year, 2 years

## Website Pages (Streamlit)

### 1. Home Page (Beranda)
- **Introduction**: Project overview and purpose
- **Disclaimer**: Risk warning for stock predictions
- **Dataset**: Used data (2022-Latest, updated daily at 00:00 WIB)
- **Methods & Models**: ML approaches used
- **Tech Stack**: Technologies and libraries
- **Credits**: Programmer/Data Science credits

### 2. Information Page (Informasi)
- Dataset information (before preprocessing)
- Dataset information (after preprocessing)
- Fixed dataset details
- Evaluation metrics for each model

### 3. Stock Charts Page (Grafik Harga Saham)
- Stock price charts for all 10 banks from 2022-present
- Interactive chart similar to trading apps
- Detailed information display
- Stock selector dropdown
- Multiple timeframe views

### 4. Prediction Page (Prediksi)
- Stock selector dropdown
- Prediction period dropdown
- Prediction results display
- Disclaimer

## Database Schema (SQLite)

### Table: stocks_data
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| ticker | TEXT | Stock ticker symbol |
| date | DATE | Date of data |
| open | REAL | Opening price |
| high | REAL | Highest price |
| low | REAL | Lowest price |
| close | REAL | Closing price |
| volume | REAL | Trading volume |
| ma_5 | REAL | 5-day Moving Average |
| ma_10 | REAL | 10-day Moving Average |
| ma_20 | REAL | 20-day Moving Average |
| ma_50 | REAL | 50-day Moving Average |
| ma_200 | REAL | 200-day Moving Average |
| ema_12 | REAL | 12-day EMA |
| ema_26 | REAL | 26-day EMA |
| macd | REAL | MACD line |
| macd_signal | REAL | MACD signal line |
| macd_hist | REAL | MACD histogram |
| vwap | REAL | VWAP |
| rsi | REAL | RSI (14) |
| stochastic_k | REAL | Stochastic %K |
| stochastic_d | REAL | Stochastic %D |
| roc | REAL | Rate of Change |
| bb_upper | REAL | Bollinger Upper |
| bb_middle | REAL | Bollinger Middle |
| bb_lower | REAL | Bollinger Lower |
| atr | REAL | Average True Range |
| volatility | REAL | Historical Volatility |
| created_at | DATETIME | Record creation time |

### Table: model_metrics
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| ticker | TEXT | Stock ticker |
| model_name | TEXT | Model name |
| mse | REAL | Mean Squared Error |
| rmse | REAL | Root Mean Squared Error |
| mae | REAL | Mean Absolute Error |
| r2_score | REAL | R² Score |
| training_date | DATE | Training date |

### Table: predictions
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| ticker | TEXT | Stock ticker |
| prediction_date | DATE | Prediction date |
| target_date | DATE | Target date for prediction |
| predicted_price | REAL | Predicted price |
| model_name | TEXT | Model used |
| created_at | DATETIME | Creation time |

## Project Structure
```
prediksi-harga-saham/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── config.py              # Configuration settings
├── database/
│   ├── __init__.py
│   ├── db_manager.py      # SQLite database management
│   └── schema.py          # Database schema definitions
├── data/
│   ├── __init__.py
│   ├── collect_data.py    # Data collection from yfinance
│   ├── indicators.py      # Technical indicators calculation
│   └── preprocess.py      # Data preprocessing
├── models/
│   ├── __init__.py
│   ├── linear_regression.py
│   ├── random_forest.py
│   ├── xgboost_model.py
│   ├── lstm_model.py
│   └── model_manager.py   # Model training and saving
├── api/
│   ├── __init__.py
│   ├── data_api.py        # Data collection API
│   ├── info_api.py        # Data information API
│   ├── preprocessing_api.py
│   ├── training_api.py    # Training API
│   ├── evaluation_api.py  # Evaluation API
│   └── predict_api.py     # Prediction API
├── pages/
│   ├── __init__.py
│   ├── 1_beranda.py      # Home page
│   ├── 2_informasi.py     # Information page
│   ├── 3_grafik.py        # Charts page
│   └── 4_prediksi.py      # Prediction page
├── utils/
│   ├── __init__.py
│   ├── validators.py      # Data validation
│   ├── visualization.py   # Chart plotting
│   └── helpers.py         # Helper functions
└── logs/
    └── app.log           # Application logs
```

## Acceptance Criteria

### Data Collection
- [ ] Successfully fetch data from yfinance for all 10 banks
- [ ] Data range from 2022-01-01 to current date
- [ ] Data stored in SQLite database
- [ ] Auto-update at 00:00 WIB

### Technical Indicators
- [ ] All 14 technical indicators calculated correctly
- [ ] Indicators stored in database

### Data Validation
- [ ] Missing value check displays results
- [ ] Duplicate check displays results
- [ ] Outlier detection working
- [ ] Range validation working
- [ ] Format consistency check working

### Preprocessing
- [ ] Missing values handled
- [ ] Duplicates removed
- [ ] Outliers handled
- [ ] Data scaled/normalised

### Model Training
- [ ] Random Forest trained
- [ ] XGBoost trained
- [ ] LSTM trained
- [ ] Models saved with Joblib

### Evaluation
- [ ] MSE calculated
- [ ] RMSE calculated
- [ ] MAE calculated
- [ ] R² Score calculated

### Streamlit Pages
- [ ] Home page displays all information
- [ ] Information page shows dataset details
- [ ] Charts page shows interactive stock charts
- [ ] Prediction page works with all time periods

### General
- [ ] Application runs without errors
- [ ] All pages accessible
- [ ] Responsive design
- [ ] Professional UI/UX
