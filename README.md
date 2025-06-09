# 📈 Stock Trading Agent (Streamlit App)

A Streamlit-based trading dashboard that combines real-time stock analysis, backtesting strategies, Alpaca paper/live trading, and Telegram alerts.

## 🚀 Features

- 📊 **Live Trading Signal Generator**
  - Strategies: SMA + MACD + RSI, or RSI-only
  - 5-minute intraday analysis
  - Latest trading signal displayed with visual indicators

- 🧠 **Backtesting Engine**
  - Compare your strategy returns vs market performance
  - Uses historical daily price data (default: 6 months)

- 🤖 **Auto-Trading Ready**
  - Integrated with [Alpaca API](https://alpaca.markets/) for live/paper trading
  - Secure API key management via `st.secrets`

- 🔔 **Telegram Alerts**
  - Sends signal updates to your configured Telegram bot/channel

- 📈 **Streamlit Cloud Deployable**
  - Cloud-ready with a simple `.streamlit/secrets.toml` setup
  - Public or private deployment

## 🧰 Project Structure

```
.
├── stock_trading_agent.py      # Main Streamlit application
├── requirements.txt            # Python dependencies
└── .streamlit/
    └── secrets.toml            # API credentials (not tracked in Git)
```

## 🔐 secrets.toml Example

```toml
TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
TELEGRAM_CHAT_ID = "your-telegram-chat-id"
ALPACA_API_KEY = "your-alpaca-api-key"
ALPACA_SECRET_KEY = "your-alpaca-secret-key"
ALPACA_ENDPOINT = "https://paper-api.alpaca.markets"
```

## 📦 Setup Instructions

```bash
git clone https://github.com/drnithyauk/stock-trading-agent.git
cd stock-trading-agent
pip install -r requirements.txt
streamlit run stock_trading_agent.py
```

## 🌐 Deploy on Streamlit Cloud

1. Push your project to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your repo and deploy `stock_trading_agent.py`

## 📩 Contact

For ideas, issues, or improvements, open an issue or connect with the developer.

---

**DISCLAIMER**: This tool is for educational and prototyping purposes only. Trade at your own risk.
