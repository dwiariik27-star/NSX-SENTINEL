import yfinance as yf
import pandas as pd

def get_live_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d", interval="15m")
        if df.empty: return "ERROR: No Data"
        
        # Hitung RSI Sederhana
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        last_price = df['Close'].iloc[-1]
        volatility = df['Close'].std()
        
        return {
            "symbol": symbol,
            "price": round(last_price, 2),
            "rsi": round(rsi.iloc[-1], 2),
            "volatility": round(volatility, 4),
            "trend": "BULLISH" if last_price > df['Close'].mean() else "BEARISH"
        }
    except Exception as e:
        return f"ERROR: {e}"
