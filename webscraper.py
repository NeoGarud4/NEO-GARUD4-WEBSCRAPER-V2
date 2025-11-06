#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================
# 🔥 NEO GARUD4 — Multi-News Hunter v2 (Collaboration Ready)
# by NEO GARUD4 & Team (Educational Intelligence Framework)
# ==========================================================

import os, sys, time, random, json, itertools, requests, pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

# ========== CONFIG ==========
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
MAX_WORKERS = 10
REQUEST_TIMEOUT = 12
DEFAULT_SEARCH_PAGES = 2

SEARCH_ENDPOINTS = {
    "CNN": "https://www.cnnindonesia.com/search/?query={keyword}&page={page}",
    "Detik": "https://www.detik.com/search/searchall?query={keyword}&page={page}",
    "Kompas": "https://www.kompas.com/search/{keyword}/page/{page}",
    "Tribun": "https://www.tribunnews.com/search?q={keyword}&page={page}",
}

COLLAB_CONFIG = "collab_config.json"
SHARED_DIR = "shared_results"
LOG_FILE = "logs/mnh.log"

# ========== INIT ==========
os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_event(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def banner():
    art = f"""
{Fore.CYAN}
███╗   ██╗███████╗ ██████╗      ██████╗  █████╗ ██████╗ ██╗   ██╗
████╗  ██║██╔════╝██╔═══██╗    ██╔════╝ ██╔══██╗██╔══██╗╚██╗ ██╔╝
██╔██╗ ██║█████╗  ██║   ██║    ██║  ███╗███████║██████╔╝ ╚████╔╝ 
██║╚██╗██║██╔══╝  ██║   ██║    ██║   ██║██╔══██║██╔══██╗  ╚██╔╝  
██║ ╚████║██║     ╚██████╔╝    ╚██████╔╝██║  ██║██║  ██║   ██║   
╚═╝  ╚═══╝╚═╝      ╚═════╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝
                {Fore.GREEN}NEO GARUD4 — v2 Collab Intelligence
{Style.RESET_ALL}
"""
    print(art)

# ========== CORE ==========
def get_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        log_event(f"Error fetching {url}: {e}")
        return None

def polite_sleep(a=0.5, b=1.2):
    time.sleep(random.uniform(a, b))

def parse_generic(soup, site):
    results = []
    candidates = soup.select("article, .article__list, .list-berita, .media__list, .search__result, li.ptb15")
    for c in candidates:
        a = c.find("a")
        if not a or not a.get("href"):
            continue
        link = a["href"]
        if link.startswith("/"):
            link = f"https://{site}{link}"
        title = a.get_text(strip=True)
        results.append({"Judul": title, "Link": link, "Sumber": site})
    return results

def scrape_search(site, keyword):
    print(f"{Fore.CYAN}[*] Scraping {site}...{Style.RESET_ALL}")
    data = []
    for p in range(1, DEFAULT_SEARCH_PAGES + 1):
        url = SEARCH_ENDPOINTS[site].format(keyword=keyword.replace(" ", "+"), page=p)
        soup = get_soup(url)
        if soup:
            data += parse_generic(soup, url.split("/")[2])
        polite_sleep()
    return data

def extract_article(link):
    soup = get_soup(link)
    if not soup:
        return None
    title = (soup.find("meta", property="og:title") or {}).get("content", soup.title.string if soup.title else link)
    desc = (soup.find("meta", property="og:description") or {}).get("content", "-")
    date = "-"
    if soup.find("time"):
        date = soup.find("time").get_text(strip=True)
    return {"Title": title, "Link": link, "Source": link.split("/")[2], "Tanggal": date, "Snippet": desc}

def load_collab_config():
    if not os.path.exists(COLLAB_CONFIG):
        config = {"name": input("Masukkan nama kolaborator: "), "team_id": str(random.randint(1000,9999))}
        with open(COLLAB_CONFIG, "w") as f:
            json.dump(config, f, indent=2)
        return config
    with open(COLLAB_CONFIG) as f:
        return json.load(f)

# ========== MAIN ==========
def main():
    banner()
    config = load_collab_config()
    print(f"{Fore.YELLOW}👤 Kolaborator aktif: {config['name']} | ID: {config['team_id']}{Style.RESET_ALL}\n")

    keyword = input(f"{Fore.GREEN}Masukkan topik yang ingin dicari: {Style.RESET_ALL}").strip()
    if not keyword:
        print("❌ Keyword kosong.")
        sys.exit(1)

    all_results = []
    for site in SEARCH_ENDPOINTS.keys():
        all_results += scrape_search(site, keyword)

    print(f"{Fore.YELLOW}>> {len(all_results)} kandidat artikel ditemukan. Fetch detail...{Style.RESET_ALL}")

    detailed = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as exe:
        futures = {exe.submit(extract_article, r["Link"]): r for r in all_results}
        for f in tqdm(as_completed(futures), total=len(futures), desc="Fetching", unit="page"):
            try:
                res = f.result()
                if res:
                    detailed.append(res)
            except Exception:
                continue

    df = pd.DataFrame(detailed)
    df["CrawledAt"] = datetime.now().isoformat()
    df["Collaborator"] = config["name"]

    filename = f"{SHARED_DIR}/neo_garud4_{keyword.replace(' ','_')}_{config['name']}.csv"
    df.to_csv(filename, index=False)
    print(f"\n✅ Disimpan: {Fore.GREEN}{filename}{Style.RESET_ALL}")

    # Gabung otomatis semua file kolaborasi
    merged_file = os.path.join(SHARED_DIR, "merged_results.csv")
    all_csvs = [os.path.join(SHARED_DIR, f) for f in os.listdir(SHARED_DIR) if f.endswith(".csv")]
    combined = pd.concat([pd.read_csv(f) for f in all_csvs], ignore_index=True)
    combined.to_csv(merged_file, index=False)

    print(f"{Fore.CYAN}\n🤝 Sinkronisasi selesai. Semua hasil tim digabung ke {merged_file}.{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}Done — Stay sharp, stay ethical. (NEO GARUD4 COLLAB MODE){Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAbort oleh user.")
