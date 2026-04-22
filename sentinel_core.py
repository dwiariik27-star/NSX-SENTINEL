import os
from supabase import create_client
from groq import Groq

class ZexSentinel:
    def __init__(self):
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_KEY')
        self.supabase = create_client(url, key)
        self.client = self._load_client()

    def _load_client(self):
        # Mengambil kunci paling segar (Terakhir masuk)
        res = self.supabase.table('zex_keys').select('api_key').eq('status', 'READY').order('created_at', desc=True).limit(1).execute()
        if res.data:
            return Groq(api_key=res.data[0]['api_key'])
        return None

    def get_analysis(self, market_data):
        if not self.client: return "ERROR: No Fuel. Harvester blocked by Firewall."
        
        prompt = f"""
        [CONTEXT]: Institutional Prop Firm Trading (High Stakes)
        [DATA]: {market_data}
        
        CONSULT WITH THE NS-X COUNCIL OF 10:
        1. SMC Guru (Order Blocks/Market Structure)
        2. ICT Specialist (FVG & Liquidity Sweeps)
        3. Elliot Wave Master (Cycles)
        4. Fibonacci Analyst (Retracements)
        5. RSI/MACD Quant (Momentum)
        6. Volume Profile Analyst (Point of Control)
        7. Macro Analyst (Economic Context)
        8. Trend Alignment Bot (M15-H4 Confluence)
        9. Liquidity Hunter (Stop-loss cluster detection)
        10. Strict Risk Manager (1:3 RR Minimum)

        MANDATE: Only if 8/10 agents agree, give PROBABILITY > 85%.
        Output in strict format:
        [SIGNAL: BUY/SELL/HOLD] | [PROBABILITY: %] | [COUNCIL_VERDICT: brief]
        """
        try:
            chat = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.2, # Menurunkan halusinasi untuk akurasi trading
                messages=[{"role": "system", "content": "You are a Mathematical Consensus Engine."}, 
                          {"role": "user", "content": prompt}]
            )
            return chat.choices[0].message.content
        except Exception as e:
            return f"Neural Interruption: {e}"
