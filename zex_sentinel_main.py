import time
from market_sensor import MarketSensor
from sentinel_core import analyze_market

def execute_sentinel_loop():
    sensor = MarketSensor()
    print("--- NS-X SENTINEL: SYSTEM ONLINE (24/7 MODE) ---")

    while True:
        for asset in ["GOLD", "EURUSD"]:
            print(f"[+] Menganalisis {asset}...")
            
            # 1. Ambil Data Real-time
            market_data = sensor.fetch_live_data(asset)
            
            if market_data:
                # 2. Kirim ke AI untuk Keputusan Institusi
                decision = analyze_market(asset, market_data)
                
                print(f"--- KEPUTUSAN UNTUK {asset} ---")
                print(decision)
                print("-" * 30)
            
            # Jeda antar aset untuk menghindari deteksi pola
            time.sleep(10)
            
        # Siklus ulang setiap 5 menit (Sesuai interval chart)
        print("[!] Siklus Selesai. Menunggu candle berikutnya...")
        time.sleep(300)

if __name__ == "__main__":
    execute_sentinel_loop()