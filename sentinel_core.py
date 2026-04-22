import os
from supabase import create_client
from groq import Groq

class ZexSentinel:
    def __init__(self):
        self.supabase = create_client(os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_KEY'))
        self.client = self._load_client()

    def _load_client(self):
        # Ambil kunci paling segar dari Sinapsis
        res = self.supabase.table('zex_keys').select('api_key').eq('status', 'READY').order('created_at', desc=True).limit(1).execute()
        if res.data:
            return Groq(api_key=res.data[0]['api_key'])
        return None

    def get_analysis(self, market_data):
        if not self.client: return "ERROR: Fuel Empty. Harvester needs to run."
        
        # SWARM ARCHITECTURE: 10 Specialist Agents
        prompt = f"""
        DATA: {market_data}
        You are the HEAD OF THE NS-X COUNCIL. Coordinate 10 Elite Agents for a Prop Firm Trade:
        1. SMC Guru, 2. ICT Expert, 3. Elliot Wave Master, 4. Fibonacci Quant, 
        5. RSI/MACD Sniper, 6. Volume Profile Analyst, 7. Macro Scout, 
        8. Trend Alignment Bot, 9. Liquidity Hunter, 10. Risk Manager.

        MANDATE: 
        - If agents are split, Probability < 70%.
        - If 8/10 agree on setup, Probability > 85%.
        - Identify "Stop Hunt" zones specifically.

        Format: [SIGNAL: BUY/SELL/HOLD] | [PROBABILITY: %] | [COUNCIL_REASON]
        """
        try:
            chat = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.1, # Mode Presisi Tinggi
                messages=[{"role": "system", "content": "You are the NS-X Sovereign Engine."}, {"role": "user", "content": prompt}]
            )
            return chat.choices[0].message.content
        except: return "Neural Link Interrupted"
