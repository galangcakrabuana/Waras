from pathlib import Path

content = r"""# WARAS-ID Database Architecture Specification v1.0

## Objective

Membangun database terpusat yang menggabungkan:

- Data BPOM
- Data WHO ATC
- Data OpenFDA
- Hasil NLP ClaimSense Engine

Tujuan utama:

Saat pengguna melakukan scan produk menggunakan:

- URL Marketplace
- Barcode
- Screenshot
- Nama Produk

Sistem dapat memberikan informasi produk secara komprehensif serta melakukan analisis risiko klaim kesehatan dalam satu kali proses.

---

## Existing Data Sources

### BPOM + WHO ATC

Tersedia file Excel gabungan yang memuat:

- Data Produk BPOM
- Data Kategori ATC WHO
- Informasi DDD
- Informasi Route Administration
- Informasi Kategori Terapi

File ini menjadi sumber utama identifikasi produk.

### OpenFDA

Menggunakan API:

https://api.fda.gov/drug/event.json

Digunakan untuk:

- Adverse Event
- Efek samping yang sering dilaporkan
- Tingkat keparahan laporan
- Statistik keamanan obat

Data tidak disimpan penuh secara lokal pada tahap awal.
Sistem melakukan request saat dibutuhkan dan menyimpan cache hasil pencarian.

---

## Database Design

### products

Master data produk.

Fields:

- id
- product_name
- registration_number
- manufacturer
- product_category
- ingredient
- atc_code
- created_at
- updated_at

### atc_reference

Referensi WHO ATC.

Fields:

- atc_code
- atc_name
- ddd
- uom
- administration_route
- note

### atc_hierarchy

Hierarki klasifikasi ATC.

Fields:

- code
- name
- level
- parent_code

Contoh:

A → A10 → A10B → A10BA → A10BA02

### adverse_event_cache

Cache OpenFDA.

Fields:

- id
- ingredient_name
- adverse_event
- occurrence_count
- severity
- last_updated

### claim_analysis

Hasil NLP.

Fields:

- id
- product_id
- analyzed_text
- prediction_label
- confidence_score
- detected_claims
- created_at

Label:

- 0 = Safe
- 1 = Ambiguous
- 2 = Overclaim

### product_analysis

Hasil analisis final.

Fields:

- id
- product_id
- claim_score
- consistency_score
- safety_score
- recommendation
- created_at

---

## Data Flow

User Input

- URL Marketplace
- Barcode
- Screenshot
- Nama Produk

↓

Product Lookup

↓

BPOM Database

↓

ATC Mapping

↓

Product Profile Generated

Output:

- Nama Produk
- Nomor BPOM
- Produsen
- Zat Aktif
- Kategori Produk
- Kategori Terapi
- DDD WHO

---

## ClaimSense Engine

Input:

- Product Title
- Product Description
- OCR Result

Model:

- IndoBERT

Output:

- 0 = Safe
- 1 = Ambiguous
- 2 = Overclaim

---

## Medical Consistency Engine

Input:

- Product Category
- ATC Category
- NLP Result

Tujuan:

Menentukan apakah klaim yang ditemukan sesuai dengan fungsi medis produk.

Contoh:

Kategori: Vitamin

Klaim: Menyembuhkan Diabetes

Hasil: Low Consistency

Output:

Consistency Score (0-100)

---

## Adverse Event Engine

Input:

Ingredient Name

↓

OpenFDA API

↓

Adverse Event Summary

Output:

- Most Reported Side Effects
- Severe Event Frequency
- Number of Reports

---

## Consumer Safety Score

Konsep:

Consumer Safety Score =

- Claim Risk Score
- Medical Consistency Score
- BPOM Verification Score
- Adverse Event Risk Score

Interpretasi:

- 0-30 = High Risk
- 31-60 = Moderate Risk
- 61-80 = Low Risk
- 81-100 = Safe

---

## Final User Output

Satu kali input menghasilkan:

### Product Profile

- Product Name
- BPOM Number
- Manufacturer
- Ingredient
- ATC Category
- DDD

### Claim Analysis

- Risk Score
- Detected Claims
- Confidence Score

### Explainable AI

- Trigger Words
- Trigger Sentences

### Medical Consistency

- Consistency Score
- Explanation

### Safety Information

- Common Side Effects
- Severe Adverse Events

### Final Recommendation

- Safe
- Need Attention
- Potential Overclaim

---

## Future Development

- Product Comparison
- Marketplace Risk Dashboard
- Claim Trend Analytics
- Product Recommendation Engine
- Public Health Intelligence Dashboard
- National Overclaim Monitoring System
"""

path = "/mnt/data/WARAS_ID_Database_Architecture.md"
Path(path).write_text(content, encoding="utf-8")
print(path)
