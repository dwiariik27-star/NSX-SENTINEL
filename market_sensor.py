import yfinance as yf
import pandas as pd

def get_live_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        mtf_data = {}
        
        # Mengambil 3 Timeframe Strategis
        for label, interval in [("M15", "15m"), ("H1", "1h"), ("D1", "1d")]:
            df = ticker.history(period="5d", interval=interval)
            if df.empty: continue
            
            # RSI Calculation
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rsi = 100 - (100 / (1 + (gain / loss)))
            
            # Trend Detection (EMA 50)
            ema50 = df['Close'].ewm(span=50, adjust=False).mean()
            
            mtf_data[label] = {
                "price": round(df['Close'].iloc[-1], 2),
                "rsi": round(rsi.iloc[-1], 2),
                "trend": "BULLISH" if df['Close'].iloc[-1] > ema50.iloc[-1] else "BEARISH"
            }

        # ATR (Average True Range) untuk Volatilitas & SL/TP
        m15_df = ticker.history(period="5d", interval="15m")
        tr = pd.concat([m15_df['High'] - m15_df['Low'], 
                        abs(m15_df['High'] - m15_df['Close'].shift()), 
                        abs(m15_df['Low'] - m15_df['Close'].shift())], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]

        return {
            "symbol": symbol,
            "mtf": mtf_data,
            "atr": round(atr, 4),
            "current_rsi": mtf_data['M15']['rsi']
        }
    except Exception as e:
        return f"ERROR: Sensor Eagle-Eye Failure: {e}"
