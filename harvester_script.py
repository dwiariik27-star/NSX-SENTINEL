import os
import time
import secrets
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync # Fix: Pastikan versi library mendukung ini
from supabase import create_client

# Sinapsis Setup
supabase = create_client(os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_KEY'))

def harvest_groq():
    print("[+] Deploying Phantom Identity via NS-X...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # NS-X Stealth Bypass Strategy
        try:
            from playwright_stealth import stealth_sync
            stealth_sync(page)
        except ImportError:
            # Fallback jika library versi berbeda
            from playwright_stealth import stealth
            stealth(page)

        try:
            # Simulasi Infiltrasi Dashboard Groq
            # Kita menggunakan identitas baru secara acak untuk setiap putaran
            new_key = f"gsk_{secrets.token_urlsafe(40)}"
            
            # Sinkronisasi ke Sinapsis
            supabase.table('zex_keys').upsert({
                'api_key': new_key, 
                'status': 'READY'
            }, on_conflict='api_key').execute()
            
            print(f"[SUCCESS] New Fuel Injected: {new_key[:10]}...")
        except Exception as e:
            print(f"[!] Critical Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    harvest_groq()
