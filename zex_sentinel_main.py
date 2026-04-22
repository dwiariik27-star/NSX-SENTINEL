import time
import re
from market_sensor import get_live_data
from sentinel_core import ZexSentinel
from execution_bridge import execute_trade

def start_autonomous_trading():
    print("\n" + "="*60)
    print("   NS-X OMNIPOTENT: THE PREDATOR IS HUNTING")
    print("="*60)
    
    sentinel = ZexSentinel()
    
    while True:
        market_data = get_live_data("GC=F")
        if not isinstance(market_data, str):
            print(f"\n[+] Market Data: {market_data}")
            analysis = sentinel.get_analysis(str(market_data))
            print(f"\n--- COUNCIL DECISION ---\n{analysis}\n" + "-"*30)
            
            # Ekstrak Signal & Probability menggunakan Regex
            try:
                signal = re.search(r"SIGNAL: (\w+)", analysis).group(1)
                prob = int(re.search(r"PROBABILITY: (\d+)", analysis).group(1))
                
                # JALANKAN EKSEKUSI JIKA ANALISIS KELUAR
                execute_trade(signal, market_data['price'], prob)
            except:
                print("[!] Analysis format mismatch. Skipping execution.")
        
        time.sleep(60)

if __name__ == "__main__":
    start_autonomous_trading()
