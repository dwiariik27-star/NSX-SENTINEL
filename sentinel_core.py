import os
import random
from supabase import create_client
from groq import Groq

# Inisialisasi Sinapsis (Supabase)
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')
supabase = create_client(url, key)

class ZexSentinel:
    def __init__(self):
        self.keys = self._get_keys_from_sinapsis()
        self.selected_key = random.choice(self.keys) if self.keys else None

    def _get_keys_from_sinapsis(self):
        # Mengambil kunci yang statusnya READY dari Supabase
        response = supabase.table('zex_keys').select('api_key').eq('status', 'READY').execute()
        return [item['api_key'] for item in response.data]

    def get_analysis(self, market_context):
        if not self.selected_key:
            return "ERROR: No API Fuel"
        
        client = Groq(api_key=self.selected_key)
        
        # PROTOKOL ZEX-SWARM: Multi-Agent Analysis Prompt
        prompt = f"""
        Act as ZEX-SWARM Intelligence. Analyze this market data: {market_context}
        1. Macro Scout: Analyze news impact.
        2. SMC Specialist: Identify Order Blocks & Liquidity.
        3. Quant Analyst: Calculate win probability.
        
        Output format: [SIGNAL: BUY/SELL/HOLD] | [PROBABILITY: %] | [REASON: brief]
        """
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"ERROR: {str(e)}"

if __name__ == "__main__":
    # Simulasi pengambilan data pasar (Nantinya akan otomatis dari Stage 3)
    sample_context = "XAUUSD at 2350.50, Bullish Order Block at 2340, FED News: Neutral"
    sentinel = ZexSentinel()
    print("--- NS-X SENTINEL ANALYSIS START ---")
    print(sentinel.get_analysis(sample_context))
