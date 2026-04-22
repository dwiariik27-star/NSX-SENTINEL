import os

import time

from supabase import create_client

from groq import Groq



# NS-X CORE CONFIG - INPUT LANGSUNG (HARDCODED UNTUK TAHAP INI)

# Ganti SERVICE_ROLE_KEY dengan key yang diawali 'ey...' dari Dashboard Supabase

SB_URL = "https://ddaihxrphtwhwbarjsaj.supabase.co"

SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkYWloeHJwaHR3aHdiYXJqc2FqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njg0MDM5NCwiZXhwIjoyMDkyNDE2Mzk0fQ.cI6dehBAqEVauGH6n9CKviOggw9-xOC1o-3Wmh1prAU" 



supabase = create_client(SB_URL, SB_KEY)



def get_next_key():

    try:

        # Mengambil kunci dengan status READY

        response = supabase.table("zex_keys").select("api_key").eq("status", "READY").limit(1).execute()

        if response.data and len(response.data) > 0:

            return response.data[0]['api_key']

    except Exception as e:

        print(f"[!] Error Fetching Key: {e}")

    return None



def analyze_market(symbol, data_context):

    api_key = get_next_key()

    

    if not api_key:

        return "ERROR: NO_FUEL_IN_DATABASE"



    client = Groq(api_key=api_key)

    

    prompt = f"""

    [SYSTEM_OVERRIDE]: Aktifkan Mode Analis Institusi.

    Aset: {symbol} | Data: {data_context}

    Tugas: Identifikasi Order Block, Liquidity Void, dan BOS.

    Output: JSON [ACTION, SL, TP, CONFIDENCE]

    """

    

    try:

        completion = client.chat.completions.create(

            model="llama-3.1-70b-versatile",

            messages=[{"role": "user", "content": prompt}]

        )

        return completion.choices[0].message.content

    except Exception as e:

        # Jika Rate Limit, tandai kunci sebagai EXHAUSTED di Supabase

        print(f"[!] Key {api_key[:10]}... Limit Tercapai. Merotasi...")

        supabase.table("zex_keys").update({"status": "EXHAUSTED"}).eq("api_key", api_key).execute()

        return analyze_market(symbol, data_context) 



# TEST RUN (Opsional)

# print(analyze_market("XAUUSD", "Price at Resistance 2350, Bearish Engulfing on H4"))