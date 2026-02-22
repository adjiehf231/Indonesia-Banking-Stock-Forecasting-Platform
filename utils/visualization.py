"""
Visualization Module - Chart and plot functions.
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional


def plot_candlestick(df: pd.DataFrame, title: str = "Candlestick Chart") -> go.Figure:
    """Create a candlestick chart."""
    fig = go.Figure(data=[
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,
        height=500
    )
    
    return fig


def plot_line(df: pd.DataFrame, columns: list, title: str = "Line Chart") -> go.Figure:
    """Create a line chart for multiple columns."""
    fig = go.Figure()
    
    for col in columns:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df[col],
                mode='lines',
                name=col
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Value",
        height=400
    )
    
    return fig


def plot_volume(df: pd.DataFrame, title: str = "Volume") -> go.Figure:
    """Create a volume bar chart."""
    fig = go.Figure(data=[
        go.Bar(
            x=df['date'],
            y=df['volume'],
            name='Volume',
            marker_color='rgba(100, 100, 100, 0.5)'
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Volume",
        height=300
    )
    
    return fig


def plot_technical_indicators(df: pd.DataFrame) -> go.Figure:
    """Create a chart with price and technical indicators."""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('Price with MA', 'MACD', 'RSI'),
        row_heights=[0.5, 0.25, 0.25]
    )
    
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['close'], name='Close', line=dict(color='black')),
        row=1, col=1
    )
    
    if 'ma_20' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['ma_20'], name='MA20', line=dict(color='blue')),
            row=1, col=1
        )
    
    if 'macd' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['macd'], name='MACD', line=dict(color='green')),
            row=2, col=1
        )
    
    if 'rsi' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['rsi'], name='RSI', line=dict(color='red')),
            row=3, col=1
        )
    
    fig.update_layout(
        height=800,
        showlegend=True
    )
    
    return fig


def plot_bollinger_bands(df: pd.DataFrame) -> go.Figure:
    """Create a chart with Bollinger Bands."""
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['close'], name='Close', line=dict(color='black'))
    )
    
    if 'bb_upper' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['bb_upper'], name='Upper Band', 
                      line=dict(color='red', dash='dash'))
        )
    
    if 'bb_middle' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['bb_middle'], name='Middle Band',
                      line=dict(color='blue'))
        )
    
    if 'bb_lower' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['bb_lower'], name='Lower Band',
                      line=dict(color='red', dash='dash'))
        )
    
    fig.update_layout(
        title="Bollinger Bands",
        xaxis_title="Date",
        yaxis_title="Price",
        height=400
    )
    
    return fig


def plot_prediction_results(actual: pd.Series, predicted: pd.Series, 
                          title: str = "Actual vs Predicted") -> go.Figure:
    """Create a chart comparing actual and predicted values."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=actual,
        mode='lines',
        name='Actual',
        line=dict(color='blue')
    ))
    
    fig.add_trace(go.Scatter(
        y=predicted,
        mode='lines',
        name='Predicted',
        line=dict(color='red', dash='dash')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Price",
        height=400
    )
    
    return fig


def plot_model_comparison(metrics_df: pd.DataFrame) -> go.Figure:
    """Create a bar chart comparing model metrics."""
    fig = go.Figure()
    
    models = metrics_df['model_name'].unique()
    
    for model in models:
        model_data = metrics_df[metrics_df['model_name'] == model]
        
        fig.add_trace(go.Bar(
            name=model,
            x=['MSE', 'RMSE', 'MAE'],
            y=[
                model_data['mse'].values[0] if 'mse' in model_data else 0,
                model_data['rmse'].values[0] if 'rmse' in model_data else 0,
                model_data['mae'].values[0] if 'mae' in model_data else 0
            ]
        ))
    
    fig.update_layout(
        title="Model Comparison",
        barmode='group',
        height=400
    )
    
    return fig
