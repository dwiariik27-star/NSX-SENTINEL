import yfinance as yf
import pandas as pd

def get_live_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d", interval="15m")
        if df.empty: return "ERROR: No Data"
        
        # Indikator Teknis untuk Swarm
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain / loss)))
        
        last_price = df['Close'].iloc[-1]
        return {
            "symbol": symbol,
            "price": round(last_price, 4),
            "rsi": round(rsi.iloc[-1], 2),
            "trend": "BULLISH" if last_price > df['Close'].mean() else "BEARISH",
            "volatility": round(df['Close'].std(), 4)
        }
    except Exception as e:
        return f"ERROR: Sensor Blind: {e}"
