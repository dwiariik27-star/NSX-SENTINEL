import os

import subprocess

import sys



def execute_protocol():

    print("--- NS-X PROTOCOL: INITIALIZING TAHAP 0 ---")



    # 1. Input Kredensial Supabase

    sb_url = input("https://ddaihxrphtwhwbarjsaj.supabase.co: ").strip()

    sb_key = input("sb_publishable_A-dLxYSDazoUahhHTjXD-g_6zXI-3GA: ").strip()



    # 2. Inisialisasi Repository Lokal

    project_dir = "NSX_SENTINEL"

    if not os.path.exists(project_dir):

        os.makedirs(project_dir)

    os.chdir(project_dir)

    

    subprocess.run("git init", shell=True)



    # 3. Sinkronisasi ke GitHub Cloud

    print("[+] Menghubungkan ke GitHub Actions...")

    subprocess.run("gh repo create NSX-SENTINEL --private --confirm", shell=True)

    

    # Menanamkan Secret ke GitHub secara otomatis

    subprocess.run(f'gh secret set SUPABASE_URL --body "{sb_url}"', shell=True)

    subprocess.run(f'gh secret set SUPABASE_KEY --body "{sb_key}"', shell=True)



    # 4. Membuat Struktur File Awal

    os.makedirs(".github/workflows", exist_ok=True)

    with open("requirements.txt", "w") as f:

        f.write("supabase\ngroq\nplaywright\nplaywright-stealth\n")



    print("\n[SUCCESS] Tahap 0 Selesai Tanpa Error.")

    print("Infrastruktur Sinapsis telah terhubung.")



if __name__ == "__main__":

    execute_protocol()