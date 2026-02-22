# 🚀 Indonesia Banking Stock Forecasting Platform

### End-to-End Machine Learning & Deep Learning System

An enterprise-style web application that forecasts stock prices for Indonesia’s top 10 banks using advanced Machine Learning and Deep Learning pipelines.

> Designed as a production-ready data science portfolio demonstrating model comparison, time-series engineering, and interactive analytics.

---

## 🎯 Executive Summary

This project delivers a full ML lifecycle implementation for financial time-series forecasting, including:

* Automated data ingestion from Yahoo Finance
* Advanced technical feature engineering
* Multi-model training pipeline
* Automatic best-model selection per ticker
* Interactive Streamlit dashboard
* Reproducible and modular architecture

The system evaluates  **Random Forest** ,  **XGBoost** , and **LSTM** models and dynamically selects the best performer for each bank based on evaluation metrics.

Proyek ini adalah aplikasi prediksi harga saham untuk 10 bank terbesar di Indonesia menggunakan berbagai teknik Machine Learning dan Deep Learning. Aplikasi ini mengambil data historis dari Yahoo Finance dan menghitung berbagai indikator teknis untuk membantu memprediksi pergerakan harga saham di masa depan.

## 🧠 Business Problem

Forecasting stock prices in emerging markets like Indonesia presents challenges:

* High volatility
* Non-stationary time series
* Market noise
* Sector-specific dynamics

This project explores how classical ML and deep learning models perform on Indonesian banking equities and builds a scalable experimentation platform.

---

## 🏦 Coverage Universe

The platform monitors Indonesia’s major banking institutions:

| Ticker | Bank                   |
| ------ | ---------------------- |
| BMRI   | Bank Mandiri           |
| BBRI   | Bank Rakyat Indonesia  |
| BBCA   | Bank Central Asia      |
| BBNI   | Bank Negara Indonesia  |
| BBTN   | Bank Tabungan Negara   |
| BRIS   | Bank Syariah Indonesia |
| BNGA   | Bank CIMB Niaga        |
| NISP   | Bank OCBC Indonesia    |
| BNLI   | Bank Permata           |
| BDMN   | Bank Danamon           |

---

## 🏗️ System Architecture

<pre class="overflow-visible! px-0!" data-start="2031" data-end="2297"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Yahoo Finance → Feature Engineering → Model Training</span><br/><span>      ↓                     ↓                  ↓</span><br/><span>   SQLite DB          Technical Indicators   Model Registry</span><br/><span>      ↓                     ↓                  ↓</span><br/><span>                Streamlit Interactive Dashboard</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### Key Design Principles

* Modular API layer
* Reproducible pipelines
* Model-agnostic framework
* Scalable for new tickers
* Production-oriented structure

---

## ⚙️ Technology Stack

### Application Layer

* **Streamlit** — Interactive analytics UI
* **Plotly** — High-performance financial charts

### Data & Processing

* **Pandas / NumPy** — Data manipulation
* **yfinance** — Market data ingestion
* **SQLite** — Lightweight persistence

### Machine Learning

* **Scikit-learn** — Random Forest
* **XGBoost** — Gradient boosting
* **TensorFlow / Keras** — LSTM networks
* **Joblib** — Model serialization

---

## 🔬 Modeling Strategy

### Implemented Models

**Random Forest**

* Robust baseline
* Handles nonlinear tabular patterns
* Low tuning sensitivity

**XGBoost**

* High-performance gradient boosting
* Strong tabular dominance
* Feature importance support

**LSTM**

* Sequential deep learning model
* Captures temporal dependencies
* Suitable for long time series

---

## 📊 Feature Engineering

The system computes a rich technical indicator set:

### Trend Features

* MA (5, 10, 20, 50, 200)
* EMA (12, 26)

### Momentum Features

* RSI
* MACD
* Stochastic Oscillator
* ROC

### Volatility Features

* Bollinger Bands
* ATR
* Historical Volatility

### Volume Features

* VWAP

---

## 🧪 Model Evaluation Framework

Models are evaluated using:

* **MAE** — Mean Absolute Error
* **RMSE** — Root Mean Squared Error
* **MSE** — Mean Squared Error
* **R² Score** — Goodness of fit

### 🏆 Automatic Model Selection

For each ticker:

<pre class="overflow-visible! px-0!" data-start="3897" data-end="3961"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Train → Evaluate → Compare → Select Best Model → Persist</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

This ensures the production model is always the top performer per asset.

- **Streamlit** - Web framework untuk Python
- **yfinance** - Pengambilan data saham dari Yahoo Finance
- **Pandas & NumPy** - Manipulasi dan analisis data
- **Scikit-learn** - Machine Learning
- **XGBoost** - Gradient Boosting
- **TensorFlow/Keras** - Deep Learning (LSTM)
- **Joblib** - Penyimpanan model
- **SQLite** - Database lokal
- **Plotly** - Visualisasi data interaktif

## 📁 Struktur Proyek

```
prediksi harga saham 10 bank terbesar diindo/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── stock_prediction.db         # SQLite database
│
├── api/                        # API modules
│   ├── __init__.py
│   ├── data_api.py            # Data collection API
│   ├── evaluation_api.py      # Model evaluation API
│   ├── info_api.py            # Information API
│   ├── predict_api.py        # Prediction API
│   ├── preprocessing_api.py   # Data preprocessing API
│   └── training_api.py        # Model training API
│
├── data/                       # Data collection & processing
│   ├── __init__.py
│   ├── collect_data.py        # Data collection from Yahoo Finance
│   ├── indicators.py          # Technical indicators calculation
│   └── preprocess.py          # Data preprocessing
│
├── database/                   # Database management
│   ├── __init__.py
│   ├── db_manager.py          # Database operations
│   └── schema.py              # Database schema
│
├── models/                     # Machine Learning models
│   ├── __init__.py
│   ├── lstm_model.py          # LSTM neural network
│   ├── model_manager.py       # Model management
│   ├── random_forest.py       # Random Forest model
│   └── xgboost_model.py       # XGBoost model
│
├── pages/                      # Streamlit pages
│   ├── __init__.py
│   ├── beranda.py            # Home page
│   ├── informasi.py          # Information page
│   ├── grafik.py             # Charts page
│   └── prediksi.py           # Prediction page
│
└── utils/                      # Utility functions
    ├── __init__.py
    ├── helpers.py            # Helper functions
    ├── validators.py         # Input validators
    └── visualization.py      # Visualization utilities
```


**Architecture highlights:**

* Clean separation of concerns
* API-driven design
* Reusable utilities
* Extensible model layer

---

## 🚀 Quick Start

### 1️⃣ Clone Repository

<pre class="overflow-visible! px-0!" data-start="4415" data-end="4472"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼ10">git</span><span> clone <your-repo-url></span><br/><span class="ͼ10">cd</span><span> <project-folder></span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### 2️⃣ Create Environment

<pre class="overflow-visible! px-0!" data-start="4502" data-end="4534"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>python </span><span class="ͼ12">-m</span><span> venv .venv</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### 3️⃣ Activate

**Windows**

<pre class="overflow-visible! px-0!" data-start="4566" data-end="4600"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>.venv\Scripts\activate</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

**Linux/Mac**

<pre class="overflow-visible! px-0!" data-start="4616" data-end="4653"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼ10">source</span><span> .venv/bin/activate</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### 4️⃣ Install Dependencies

<pre class="overflow-visible! px-0!" data-start="4685" data-end="4728"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>pip install </span><span class="ͼ12">-r</span><span> requirements.txt</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### 5️⃣ Initialize Database

<pre class="overflow-visible! px-0!" data-start="4759" data-end="4788"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>python init_db.py</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### 6️⃣ Launch App

<pre class="overflow-visible! px-0!" data-start="4810" data-end="4842"><div class="w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-0 bottom-96"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-bg-elevated-secondary"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>streamlit run app.py</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

## 🖥️ Application Features

### 📊 Interactive Market Dashboard

* Candlestick charts
* Technical overlays
* Multi-bank comparison

### 🤖 Multi-Model Training

* Automated training pipeline
* Per-ticker evaluation
* Model persistence

### 🔮 Forecasting Engine

* Multi-horizon prediction
* Historical vs predicted visualization
* Best-model routing

### 📈 Analytics & Insights

* Dataset diagnostics
* Model metrics
* Descriptive statistics

---

## 🧩 Engineering Highlights

* End-to-end ML pipeline
* Modular API architecture
* Production-style project layout
* Model benchmarking framework
* Interactive financial visualization
* Scalable to additional assets

---

## ⚠️ Risk Disclaimer

**Important Notice**

This project is for educational and research purposes only.

* Not financial advice
* Markets are inherently risky
* Past performance ≠ future results
* Always conduct independent research
* Consult licensed financial professionals

The author assumes no liability for investment decisions.

---

## 👨‍💻 Author

**Adjie Hari Fajar**

Data Science | Machine Learning | Financial Analytics

---

## 🌟 Future Improvements (Roadmap)

* Walk-forward validation
* Hyperparameter optimization
* Transformer-based models
* Live market streaming
* Portfolio backtesting
* Cloud deployment pipeline
#   I n d o n e s i a - B a n k i n g - S t o c k - F o r e c a s t i n g - P l a t f o r m  
 