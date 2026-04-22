import os
import random
from supabase import create_client
from groq import Groq

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')
supabase = create_client(url, key)

class ZexSentinel:
    def __init__(self):
        self.keys = self._get_keys_from_sinapsis()
        self.selected_key = self.keys[0] if self.keys else None

    def _get_keys_from_sinapsis(self):
        res = supabase.table('zex_keys').select('api_key').eq('status', 'READY').execute()
        return [item['api_key'] for item in res.data]

    def get_analysis(self, market_data):
        if not self.selected_key: return "ERROR: No Fuel"
        client = Groq(api_key=self.selected_key)
        
        # PROMPT NS-X 2.5: THE AGGRESSIVE JUDGE
        prompt = f"""
        STRICT ANALYSIS REQUIRED. Market Data: {market_data}
        
        As a Master Prop Firm Trader, evaluate the probability of a winning trade.
        BE CRITICAL. If data is insufficient, probability MUST be below 50%.
        To reach >80%, you must have alignment between Trend, RSI, and SMC Order Blocks.
        
        Format: [SIGNAL: BUY/SELL/HOLD] | [PROBABILITY: %] | [STRICT_REASON]
        """
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "You are a cold, mathematical trading engine. No fluff."},
                          {"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
        except: return "ERROR: Neural Link Failed"
