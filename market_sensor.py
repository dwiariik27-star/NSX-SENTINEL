import yfinance as yf
import pandas as pd

class MarketSensor:
    def __init__(self):
        # Target utama: Gold (XAUUSD) dan Major Forex
        self.targets = {
            "GOLD": "GC=F",
            "EURUSD": "EURUSD=X",
            "GBPUSD": "GBPUSD=X"
        }

    def fetch_live_data(self, asset_key):
        ticker_symbol = self.targets.get(asset_key)
        if not ticker_symbol:
            return None
        
        # Menarik data 1 jam terakhir dengan interval 5 menit (SMC Optimized)
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period="1d", interval="5m").tail(10)
        
        # Konversi ke format string untuk konsumsi AI
        data_summary = df[['Open', 'High', 'Low', 'Close']].to_string()
        return data_summary

# TEST SENSOR
# sensor = MarketSensor()
# print(sensor.fetch_live_data("GOLD"))