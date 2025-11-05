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

