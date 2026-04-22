
import time

import sys

from market_sensor import get_live_price

from sentinel_core import ZexSentinel



def start_autonomous_trading():

    print("\n" + "="*50)

    print("   NS-X ZEX-SENTINEL: THE PREDATOR IS ONLINE")

    print("="*50)

    

    try:

        sentinel = ZexSentinel()

    except Exception as e:

        print(f"[!] Critical Error: Gagal inisialisasi Otak: {e}")

        return



    while True:

        # 1. SENSING: Lihat Harga Gold (Future)

        print("\n[+] SENSING: Menghubungi Sensor Cloud...")

        market_data = get_live_price("GC=F")

        

        if isinstance(market_data, str) and "ERROR" in market_data:

            print(f"[!] Sensor Blind: {market_data}")

        else:

            current_price = market_data.get('price', 'N/A')

            print(f"[>] Market Price (Gold): ${current_price}")

            

            # 2. THINKING: Kirim Data ke Otak Llama-3.3

            print("[+] THINKING: Menganalisis dengan ZEX-SWARM Intelligence...")

            analysis = sentinel.get_analysis(str(market_data))

            

            print(f"\n--- LOGIKA NS-X ---")

            print(analysis)

            print("-" * 20)

        

        # 3. IDLE: Jeda agar tidak terkena Rate Limit API

        print("\n[IDLE] Menunggu siklus berikutnya (60 detik)...")

        time.sleep(60)



if __name__ == "__main__":

    start_autonomous_trading()

