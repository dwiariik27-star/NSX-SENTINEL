import time
import re
from market_sensor import get_live_data
from sentinel_core import ZexSentinel
from execution_bridge import execute_trade

def start_autonomous_trading():
    print("\n" + "="*60)
    print("   NS-X SOVEREIGN: AGGRESSIVE EXTRACTION MODE")
    print("="*60)
    
    sentinel = ZexSentinel()
    
    while True:
        market_data = get_live_data("GC=F")
        if not isinstance(market_data, str):
            print(f"\n[+] Market Data: {market_data}")
            analysis = sentinel.get_analysis(str(market_data))
            
            print(f"\n--- COUNCIL DECISION ---\n{analysis}\n" + "-"*30)
            
            # LOGIKA EKSTRAKSI AGRESIF (Mencari keyword tanpa peduli simbol)
            # Mencari BUY/SELL/HOLD yang didahului oleh kata SIGNAL
            signal_search = re.search(r"SIGNAL[\W_]*(BUY|SELL|HOLD)", analysis, re.IGNORECASE)
            # Mencari angka yang didahului oleh kata PROBABILITY
            prob_search = re.search(r"PROBABILITY[\W_]*(\d+)", analysis, re.IGNORECASE)
            
            if signal_search and prob_search:
                signal = signal_search.group(1).upper()
                prob = int(prob_search.group(1))
                
                print(f"[PROCESS] Success! Captured: {signal} ({prob}%)")
                
                # Kirim ke Jembatan Eksekusi
                execute_trade(signal, market_data['mtf']['M15']['price'], prob)
            else:
                print("[!] EXTRACTION FAILED: AI Brain used an unrecognized format.")
                print("[DEBUG] Raw output snippet:", analysis[:100] + "...")
        
        print("\n[IDLE] Scanning market in 60s...")
        time.sleep(60)

if __name__ == "__main__":
    start_autonomous_trading()
