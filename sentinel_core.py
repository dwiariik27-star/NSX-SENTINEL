import os
from dotenv import load_dotenv
from supabase import create_client
from groq import Groq

load_dotenv()

class ZexSentinel:
    def __init__(self):
        self.supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
        self.client = self._load_client()

    def _load_client(self):
        res = self.supabase.table('zex_keys').select('api_key').eq('status', 'READY').order('created_at', desc=True).limit(1).execute()
        if res.data:
            return Groq(api_key=res.data[0]['api_key'])
        return None

    def get_analysis(self, market_data):
        if not self.client: return "ERROR: Fuel Empty."
        
        # PROMPT NS-X SOVEREIGN: WEIGHTED SWARM MODE
        prompt = f"""
        [DEEP SCAN DATA]: {market_data}
        
        You are the NS-X Sovereign Engine. Execute a High-Probability Trade Analysis:
        
        1. MTF ALIGNMENT CHECK: Compare Trend & RSI across M15, H1, and D1.
        2. SMC/ICT WEIGHTED VOTE: Prioritize Order Blocks and FVG (Weight: 3x).
        3. MOMENTUM VOTE: RSI & ATR analysis (Weight: 1x).
        4. CONFLUENCE RULE: Probability > 85% ONLY IF M15 trend aligns with H1 or D1.
        
        CRITICAL: If the signal is against the D1 (Daily) Trend, max probability is 60%.
        Identify "SMART MONEY TRAP" areas where RSI is oversold but Trend is still strongly Bearish.

        Format Output: 
        [SIGNAL: BUY/SELL/HOLD] | [PROBABILITY: %] 
        [CONFLUENCE]: (Are timeframes aligned?)
        [VONIS_DEWAN]: (Short summary of expert debate)
        """
        try:
            chat = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.05, # Presisi maksimal, nol halusinasi
                messages=[{"role": "system", "content": "You are a Cold Mathematical Quantitative Analyst."}, 
                          {"role": "user", "content": prompt}]
            )
            return chat.choices[0].message.content
        except: return "Neural Link Interrupted."
