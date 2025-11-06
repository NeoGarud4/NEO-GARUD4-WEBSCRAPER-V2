<img width="1536" height="1024" alt="webscraper" src="https://github.com/user-attachments/assets/961d441b-db87-477b-80de-603d72dc7540" />

# NEO GARUD4 — WEBSCRAPER V2

 WEBSCRAPER yang ditujukan untuk mengumpulkan kandidat artikel dari beberapa portal berita
dan mengekstrak metadata dasar (judul, link, tanggal, snippet). Dirancang sebagai alat kolaboratif sederhana
dengan output CSV per-run dan opsi sinkronisasi hasil.

> This tool is released for educational and research purposes. Use responsibly and follow each site's robots.txt and terms of service.

## Fitur utama

- Scraping search results dari beberapa sumber (CNN Indonesia, Detik, Kompas, Tribun).
- Ekstraksi metadata artikel (title, description, tanggal bila tersedia).
- Konkurensi menggunakan ThreadPoolExecutor untuk mempercepat fetching.
- Output CSV per-run, dan opsi penggabungan otomatis (`shared_results/merged_results.csv`).
- Config sederhana (`collab_config.json`) untuk menyimpan nama kolaborator.
- Logging ke file (`logs/neo_garud4.log`).

## Struktur proyek

<img width="1366" height="616" alt="Screenshot_2025-11-05_19_41_03" src="https://github.com/user-attachments/assets/e413a8c6-9b28-4d56-98a7-0ab2a5e4053c" />

<img width="1366" height="418" alt="Screenshot_2025-11-05_19_41_34" src="https://github.com/user-attachments/assets/9efb12ee-11e4-48f3-9523-d0668a3cd97c" />

## Command Run Linux/macOS
git clone https://github.com/NeoGarud4/NEO-GARUD4-WEBSCRAPER-V2.git
cd NEO-GARUD4-WEBSCRAPER-V2
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 webscraper.py

## Command Run Windows (PowerShell)
git clone https://github.com/NeoGarud4/NEO-GARUD4-WEBSCRAPER-V2.git
chmod +x NEO-GARUD4-WEBSCRAPER-V2
cd NEO-GARUD4-WEBSCRAPER-V2
python -m venv venv
.\venv\Scripts\Activate.ps1   # atau .\venv\Scripts\activate.bat untuk cmd
pip install --upgrade pip
pip install -r requirements.txt
python3 webscraper.py


