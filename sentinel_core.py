
import os

from dotenv import load_dotenv

from supabase import create_client

from groq import Groq



load_dotenv() # Mengambil kredensial dari file .env secara otomatis



class ZexSentinel:

    def __init__(self):

        url = os.getenv('SUPABASE_URL')

        key = os.getenv('SUPABASE_KEY')

        if not url or not key:

            raise ValueError("CRITICAL: Kredensial .env tidak ditemukan!")

        self.supabase = create_client(url, key)

        self.client = self._load_client()



    def _load_client(self):

        res = self.supabase.table('zex_keys').select('api_key').eq('status', 'READY').order('created_at', desc=True).limit(1).execute()

        if res.data:

            return Groq(api_key=res.data[0]['api_key'])

        return None



    def get_analysis(self, market_data):

        if not self.client: return "ERROR: Fuel Empty. Harvester needs to run at Cloud."

        

        # PROMPT DEWAN 10 AGEN: POWERFULL MODE

        prompt = f"""

        DATA PASAR: {market_data}

        Lakukan Sidang Pleno Dewan 10 Agen NS-X:

        1. SMC (Order Blocks), 2. ICT (FVG/Liquidity), 3. Elliot Wave (Cycles), 

        4. Fibonacci (Levels), 5. RSI/MACD (Momentum), 6. Volume Profile (POC), 

        7. Macro (News Impact), 8. Trend Align (Multi-TF), 9. Liquidity Hunter (Stop Hunt), 

        10. Risk Manager (1:3 RR Requirement).



        ATURAN KETAT: 

        - Jika hanya 5 agen setuju, Probability = 50%.

        - Jika 9-10 agen setuju secara matematis, Probability > 85%.

        - Jika ada divergensi RSI vs Price, kurangi Probability secara drastis.



        Format Output: [SIGNAL: BUY/SELL/HOLD] | [PROBABILITY: %] | [VONIS_DEWAN: penjelasan singkat tiap agen]

        """

        try:

            chat = self.client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                temperature=0.1,

                messages=[{"role": "system", "content": "You are the NS-X Supreme Consensus Engine."}, 

                          {"role": "user", "content": prompt}]

            )

            return chat.choices[0].message.content

        except: return "Neural Link Interrupted."

