
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests

# Optional: for paper/live trading
from alpaca_trade_api.rest import REST, TimeFrame

# Define key parameters
TICKERS = ['AAPL', 'TSLA', 'MSFT', 'NVDA', 'AMZN']
INTERVAL = '5m'
PERIOD = '1d'
MAX_RISK_PER_TRADE = 0.01
CAPITAL = 100000
TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
ALPACA_API_KEY = st.secrets["ALPACA_API_KEY"]
ALPACA_SECRET_KEY = st.secrets["ALPACA_SECRET_KEY"]
ALPACA_ENDPOINT = st.secrets.get("ALPACA_ENDPOINT", "https://paper-api.alpaca.markets")

alpaca = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPACA_ENDPOINT)

# Historical backtest data
def get_historical_data(ticker, period='6mo', interval='1d'):
    df = yf.download(ticker, period=period, interval=interval)
    df['Ticker'] = ticker
    return df

# Strategy selector
def generate_signals(df, strategy='SMA_MACD_RSI'):
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['Signal'] = 0

    if strategy == 'SMA_MACD_RSI':
        df.loc[(df['SMA_5'] > df['SMA_20']) & (df['MACD'] > df['Signal_Line']) & (df['RSI'] < 70), 'Signal'] = 1
        df.loc[(df['SMA_5'] < df['SMA_20']) & (df['MACD'] < df['Signal_Line']) & (df['RSI'] > 30), 'Signal'] = -1
    elif strategy == 'RSI_only':
        df.loc[df['RSI'] < 30, 'Signal'] = 1
        df.loc[df['RSI'] > 70, 'Signal'] = -1

    return df

# Backtesting
def backtest_strategy(df):
    df['Position'] = df['Signal'].shift(1)
    df['Returns'] = df['Close'].pct_change()
    df['Strategy'] = df['Position'] * df['Returns']
    df['Cumulative Market Returns'] = (1 + df['Returns']).cumprod()
    df['Cumulative Strategy Returns'] = (1 + df['Strategy']).cumprod()
    return df

# Streamlit App
st.title("Backtesting and Live Trading Dashboard")
selected_ticker = st.selectbox("Select Ticker", TICKERS)
strategy = st.selectbox("Select Strategy", ['SMA_MACD_RSI', 'RSI_only'])

# Historical Backtest
hist_data = get_historical_data(selected_ticker)
hist_data = generate_signals(hist_data, strategy)
bt = backtest_strategy(hist_data)
st.subheader("Backtest Results")
st.line_chart(bt[['Cumulative Market Returns', 'Cumulative Strategy Returns']])

# Live Run
if st.button("Run Live Agent"):
    df_live = get_historical_data(selected_ticker, period='5d', interval='5m')
    df_live = generate_signals(df_live, strategy)
    latest = df_live.iloc[-1]
    st.write("Latest Signal:", 'BUY' if latest['Signal'] == 1 else 'SELL' if latest['Signal'] == -1 else 'HOLD')
