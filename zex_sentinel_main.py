import time
from market_sensor import get_live_data
from sentinel_core import ZexSentinel

def start_autonomous_trading():
    print("\n" + "="*60)
    print("   NS-X OMNIPOTENT: THE COUNCIL OF 10 IS LIVE")
    print("="*60)
    
    sentinel = ZexSentinel()
    
    while True:
        print("\n[+] SENSING: Scanning Market with Technical Indicators...")
        market_data = get_live_data("GC=F") # Gold Futures
        
        if isinstance(market_data, str) and "ERROR" in market_data:
            print(f"[!] Error: {market_data}")
        else:
            print(f"[>] Data Acquired: {market_data}")
            print("[+] SWARM: Consulting with the Council of 10...")
            analysis = sentinel.get_analysis(str(market_data))
            
            print(f"\n--- COUNCIL DECISION ---")
            print(analysis)
            print("-" * 30)
        
        time.sleep(60)

if __name__ == "__main__":
    start_autonomous_trading()
