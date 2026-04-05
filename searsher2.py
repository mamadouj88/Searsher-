import os
import sys
import subprocess
import threading

# Auto install modules
modules = ["requests", "colorama", "pyfiglet", "bs4"]

for m in modules:
    try:
        __import__(m)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", m])

import requests
from colorama import Fore, Style
import pyfiglet
from bs4 import BeautifulSoup

# Banner
def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + pyfiglet.figlet_format("SEARSHER", font="slant"))
    print(Fore.BLUE + ">> ADVANCED OSINT TOOL (LEGAL USE ONLY) <<\n" + Style.RESET_ALL)

# Username scan (multi-thread)
def check_site(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            print(Fore.GREEN + f"[FOUND] {url}")
    except:
        pass

def username_scan():
    username = input("Username: ")
    sites = [
        f"https://github.com/{username}",
        f"https://twitter.com/{username}",
        f"https://instagram.com/{username}",
        f"https://reddit.com/user/{username}",
        f"https://tiktok.com/@{username}"
    ]

    print("\n[+] Scan en cours...\n")

    threads = []
    for site in sites:
        t = threading.Thread(target=check_site, args=(site,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

# Email intel
def email_lookup():
    email = input("Email: ")
    print(Fore.CYAN + "\n[+] Infos email:")
    print(f"Domain: {email.split('@')[-1]}")
    print(f"Gravatar: https://www.gravatar.com/avatar/")
    print("Tip: utilise HIBP API pour leaks")

# Domain intel
def domain_lookup():
    domain = input("Domain: ")
    print(Fore.CYAN + "\n[+] WHOIS:")
    os.system(f"whois {domain}")

    try:
        print("\n[+] Headers:")
        r = requests.get(f"http://{domain}")
        for k, v in r.headers.items():
            print(f"{k}: {v}")
    except:
        print("Erreur headers")

# IP lookup
def ip_lookup():
    ip = input("IP: ")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        print(Fore.CYAN + "\n[+] Infos IP:")
        for k, v in r.items():
            print(f"{k}: {v}")
    except:
        print("Erreur")

# DuckDuckGo scraping
def duckduckgo_search():
    query = input("Recherche: ")
    url = f"https://duckduckgo.com/html/?q={query}"

    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        print(Fore.CYAN + "\n[+] Résultats:\n")
        for a in soup.find_all("a", class_="result__a", limit=5):
            print(a.get_text(), "->", a.get("href"))
    except:
        print("Erreur scraping")

# Metadata extractor
def extract_metadata():
    url = input("URL: ")
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        print(Fore.CYAN + "\n[+] Metadata:")
        print("Title:", soup.title.string if soup.title else "N/A")

        for meta in soup.find_all("meta"):
            if meta.get("name"):
                print(meta.get("name"), ":", meta.get("content"))
    except:
        print("Erreur")

# Google dorks
def google_dork():
    target = input("Target: ")
    print("\n[+] Dorks:")
    print(f"site:{target}")
    print(f"site:{target} filetype:pdf")
    print(f"site:{target} intitle:index of")
    print(f"site:{target} inurl:login")

# Menu
def menu():
    while True:
        print(Fore.BLUE + """
1. Username scan
2. Email intel
3. Domain intel
4. IP lookup
5. DuckDuckGo search
6. Metadata extractor
7. Google dorks
8. Quit
""" + Style.RESET_ALL)

        choice = input(">> ")

        if choice == "1":
            username_scan()
        elif choice == "2":
            email_lookup()
        elif choice == "3":
            domain_lookup()
        elif choice == "4":
            ip_lookup()
        elif choice == "5":
            duckduckgo_search()
        elif choice == "6":
            extract_metadata()
        elif choice == "7":
            google_dork()
        elif choice == "8":
            break
        else:
            print("Choix invalide")

if __name__ == "__main__":
    banner()
    menu()