import yfinance as yf

def get_live_price(symbol):
    try:
        # Untuk Gold gunakan GC=F (Gold Future) atau XAUUSD=X
        ticker = yf.Ticker(symbol)
        data = ticker.fast_info
        return {
            "symbol": symbol,
            "price": data['last_price'],
            "high": data['day_high'],
            "low": data['day_low']
        }
    except Exception as e:
        return f"ERROR: Sensor Blind: {e}"

if __name__ == "__main__":
    print("--- NS-X MARKET SENSOR: LIVE DATA ---")
    # Tes sensor pada Gold (XAU/USD)
    print(get_live_price("GC=F"))
