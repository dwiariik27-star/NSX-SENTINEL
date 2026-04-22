import os
from supabase import create_client
from groq import Groq

supabase = create_client(os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_KEY'))

class ZexSentinel:
    def __init__(self):
        res = supabase.table('zex_keys').select('api_key').eq('status', 'READY').execute()
        self.keys = [item['api_key'] for item in res.data]
        self.client = Groq(api_key=self.keys[0]) if self.keys else None

    def get_analysis(self, market_data):
        if not self.client: return "ERROR: No Fuel"

        # DEWAN 10 AGEN NS-X
        prompt = f"""
        [MARKET DATA]: {market_data}
        
        You are the Head of NS-X SWARM COUNCIL. Consult with these 10 specialists:
        1. SMC Master: Identify Order Blocks & Inducements.
        2. ICT Specialist: Find Silver Bullet setups & FVG.
        3. Gann Analyst: Calculate geometric price cycles.
        4. Elliot Wave Expert: Determine current wave (1-5/ABC).
        5. Macro Scout: Analyze interest rate & inflation impact.
        6. Liquidity Hunter: Locate stop-loss clusters (Buy/Sell Side).
        7. Quant Engine: Calculate standard deviation & Mean Reversion.
        8. Sentiment Bot: Scrape retail positioning (Contrarian).
        9. Trend Follower: Check H4/D1 EMA alignment.
        10. Risk Manager: Validate R:R (must be min 1:3).

        INSTRUCTION: Each agent must vote. 
        Final Probability = (Positive Votes / 10) * 100.
        Output MUST be in this exact format:
        [SIGNAL: BUY/SELL/HOLD] | [PROBABILITY: %] | [COUNCIL_REASON: brief summary of each agent's view]
        """
        
        try:
            chat = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Strict Mathematical Swarm Council Mode."},
                          {"role": "user", "content": prompt}]
            )
            return chat.choices[0].message.content
        except: return "Neural Link Interrupted"
