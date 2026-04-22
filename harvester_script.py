import os
import sys
from supabase import create_client

# NS-X NEURAL LINK
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")

if not URL or not KEY:
    print("[FATAL] Sinapsis Terputus: SUPABASE_URL/KEY Tidak Ditemukan!")
    sys.exit(1)

try:
    supabase = create_client(URL, KEY)
    # Logika pendaftaran otonom tetap di sini
    print("[+] NS-X Harvester Siap Beroperasi...")
except Exception as e:
    print(f"[!] Kegagalan Sistem: {e}")