import os
import random
import time
from supabase import create_client
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

# Sinapsis Supabase
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')
supabase = create_client(url, key)

def save_to_supabase(api_key):
    try:
        data = {'api_key': api_key, 'status': 'READY'}
        supabase.table('zex_keys').upsert(data, on_conflict='api_key').execute()
        print(f'[NS-X] Key Berhasil Disinkronkan: {api_key[:10]}...')
    except Exception as e:
        print(f'[ERROR] Gagal Simpan: {e}')

def start_harvesting():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        stealth_sync(page)

        print('[+] Memulai Operasi Pendaftaran Otomatis...')
        # Simulasi Ekstraksi Key untuk pengujian koneksi sinapsis
        fake_key = f'gsk_{random.getrandbits(160):x}'
        
        save_to_supabase(fake_key)
        browser.close()

if __name__ == '__main__':
    start_harvesting()
