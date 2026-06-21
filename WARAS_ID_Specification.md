# Spesifikasi Lengkap Platform WARAS.ID

WARAS.ID adalah platform analisis keselamatan konsumen bertenaga AI yang dirancang untuk membantu pengguna awam mengidentifikasi keabsahan produk kesehatan, memverifikasi registrasi BPOM, serta mendeteksi klaim kesehatan yang berlebihan (*overclaim*) pada promosi produk secara cepat dan transparan dalam satu halaman laporan keputusan (*decision report*).

---

## 1. Arsitektur Sistem & Integrasi Teknologi

WARAS.ID menggabungkan berbagai teknologi modern di sisi frontend, backend, dan kecerdasan buatan untuk menghasilkan analisis terpadu:

*   **Frontend**: Dibangun menggunakan HTML5 Semantis, Vanilla CSS (menggunakan palet warna kustom modern: latar belakang minty `#f2faf9`, teks gelap `#060e0e`, warna utama toska `#5abcbd`, warna sekunder slate-blue `#9bacd7`, dan aksen lavender `#7279c6`), serta Vanilla JavaScript tanpa framework tambahan untuk menjaga performa pemuatan.
*   **Backend Server**: Menggunakan Flask (Python) yang bertindak sebagai API gateway untuk memproses input, melakukan scraping, menjalankan OCR, mengkueri database lokal, serta memanggil API eksternal.
*   **Database Terpusat**: Menggunakan SQLite (`waras_id.db`) yang menyimpan data produk BPOM terintegrasi dengan klasifikasi ATC WHO.
*   **NLP ClaimSense Engine**: Menggunakan model *Deep Learning* IndoBERT Sequence Classification yang telah dilatih secara khusus untuk mendeteksi *overclaim* dalam bahasa Indonesia.
*   **OCR Reader**: Menggunakan pustaka EasyOCR untuk mengekstrak teks dari gambar promosi secara offline di sisi server.
*   **Web Scraping & CDP Integration**: Menggunakan Playwright Stealth Fetcher yang terhubung dengan Google Chrome via Chrome Debugging Protocol (CDP) di port 9222 untuk mengekstrak deskripsi produk dari platform e-commerce (Shopee) secara aman.
*   **OpenFDA API Integration**: Terhubung langsung dengan API global Food and Drug Administration (`https://api.fda.gov/drug/event.json`) untuk mengambil data efek samping (*adverse events*) secara real-time berdasarkan bahan aktif produk.

---

## 2. Fitur-Fitur Utama Platform

Platform WARAS.ID terbagi menjadi dua fungsionalitas utama di halaman input: **Periksa Klaim Produk** dan **Cek Identitas Produk**.

### A. Fitur Pemeriksaan Klaim Produk (Claim Analysis)
Fitur ini dirancang untuk mendeteksi apakah kalimat promosi, deskripsi, atau materi iklan suatu produk kesehatan mengandung klaim berlebihan yang tidak ilmiah atau berbahaya. Fitur ini menyediakan 4 metode input:

1.  **Metode Link Produk (Shopee URL)**
    *   Pengguna menempelkan URL halaman produk dari e-commerce Shopee (mendukung URL pendek berformat `shp.ee` atau `id.shp.ee`).
    *   Backend secara otomatis melakukan resolusi redirect HTTP untuk mendapatkan URL penuh produk.
    *   Sistem mengekstrak `shopid` dan `itemid` menggunakan regular expression (regex).
    *   Sistem mencoba memanggil API publik Shopee. Jika gagal (misalnya karena blokir bot/Cloudflare), sistem secara otomatis beralih menggunakan Playwright Stealth Fetcher melalui CDP (Chrome Debugging Port) untuk mensimulasikan browser manusia, mengambil judul dan deskripsi produk, lalu mengirimkannya ke mesin analisis.
2.  **Metode Foto Barcode (Barcode Scanner)**
    *   Pengguna mengunggah foto barcode dari kemasan produk fisik.
    *   Backend menggunakan pemrosesan gambar untuk membaca kode numerik barcode tersebut.
    *   Kode barcode tersebut kemudian digunakan untuk mencari data registrasi produk langsung ke database BPOM lokal.
3.  **Metode Gambar Iklan (OCR Analysis)**
    *   Pengguna mengunggah gambar promosi, poster, selebaran, atau screenshot iklan produk.
    *   Server menjalankan mesin EasyOCR untuk memindai gambar, mendeteksi teks di dalamnya, dan mengekstrak teks tersebut ke bentuk string mentah untuk dianalisis oleh model NLP.
4.  **Metode Teks Klaim (Manual Input)**
    *   Pengguna menyalin dan menempelkan teks deskripsi produk atau kalimat promosi secara langsung ke dalam kotak teks (*textarea*).
    *   Dilengkapi dengan penghitung karakter dinamis secara real-time.

### B. Fitur Cek Identitas Produk (BPOM Verification)
Tujuan fitur ini adalah memverifikasi keaslian produk kesehatan dengan database BPOM tanpa harus menguji klaim iklannya secara mendalam. Fitur ini meminimalkan bias bahwa "produk yang terdaftar pasti 100% aman iklannya". Sisi input menyediakan 2 metode pencarian:

1.  **Pencarian Teks (Text Search)**
    *   Kolom input tunggal yang mendukung pencarian berdasarkan **Nama Produk**, **Nama Bahan Aktif**, atau **Nomor Registrasi BPOM** (misal: `Paracetamol 500 mg` atau `DKL1234567890A1`).
2.  **Pencarian Barcode (Barcode Search)**
    *   Pengguna mengunggah gambar barcode produk untuk dicari langsung ke database identitas produk.

**Hasil Cek Identitas Produk** menampilkan informasi awal yang ringkas:
*   **Status Ditemukan**: Menampilkan detail data BPOM (Nama produk, Nomor registrasi, Kategori, Produsen, Bahan aktif) serta status kecocokan data (*Sesuai* atau *Cocok sebagian*).
*   **Status Tidak Ditemukan**: Memberikan panduan ejaan atau alternatif unggah foto barcode jika data produk belum terdaftar.
*   **Status Cocok Sebagian**: Peringatan jika nomor registrasi terdaftar namun nama produk atau produsen berbeda dari yang diinput pengguna.
*   **CTA Integrasi**: Tombol "Periksa klaim produk ini" yang secara otomatis memindahkan pengguna ke tab pemeriksaan klaim dengan mengisi nama produk sebagai teks analisis awal untuk mempermudah alur pemeriksaan lanjutan.

---

## 3. Mesin Analisis Di Balik Layar (Backend Engine)

### A. IndoBERT ClaimSense Engine
*   Menerima teks deskripsi produk, hasil ekstraksi OCR dari gambar iklan, atau teks input manual.
*   Model IndoBERT Sequence Classification melakukan tokenisasi teks dan menghasilkan probabilitas kelas *Overclaim* vs *Normal Claim*.
*   **Regex Trigger Extractor**: Server memindai teks untuk mendeteksi *trigger words* (kata pemicu *overclaim*) yang bersifat absolut atau tidak wajar dalam dunia medis (seperti: `sembuh total`, `tanpa efek samping`, `ampuh`, `permanen`, `100% aman`, `mujarab`, `instan`).
*   **Sentence Matcher**: Server memotong teks berdasarkan tanda baca kalimat dan mencocokkan kalimat mana saja yang memuat kata pemicu tersebut untuk ditampilkan sebagai bukti klaim kepada pengguna.

### B. Interpretasi Kode Registrasi BPOM
Mesin ini menganalisis awalan huruf (*prefix*) pada nomor registrasi BPOM untuk memberikan penjelasan fungsional kepada pengguna awam:
*   **Kode Tradisional/Herbal/Suplemen/Kosmetik (2 Huruf)**:
    *   `TR`: Obat Tradisional Lokal (Jamu Dalam Negeri)
    *   `TI`: Obat Tradisional Impor
    *   `HT`: Obat Herbal Terstandar (OHT)
    *   `FF`: Fitofarmaka (Herbal Teruji Klinis)
    *   `SD`: Suplemen Kesehatan Lokal
    *   `SI`: Suplemen Kesehatan Impor
    *   `NA` s.d `NE`: Kosmetik Lokal / Impor
*   **Obat Modern / Farmasi (3 Huruf)**:
    *   *Huruf Pertama (Penamaan)*: `D` = Obat Paten (Nama Dagang), `G` = Obat Generik.
    *   *Huruf Kedua (Keamanan/Golongan)*: `B` = Bebas, `T` = Bebas Terbatas, `K` = Obat Keras (Wajib Resep Dokter), `P` = Psikotropika, `N` = Narkotika.
    *   *Huruf Ketiga (Asal)*: `L` = Buatan Lokal, `I` = Buatan Impor.

### C. Medical Consistency Engine
Mesin ini membandingkan kesesuaian antara klaim promosi dengan jenis terapi medis produk yang terdaftar:
*   Sistem mendeteksi keberadaan kata kunci penyakit berat/kronis (seperti: `diabetes`, `stroke`, `kanker`, `jantung`, `ginjal`, `katarak`) di dalam teks promosi.
*   Jika kategori produk adalah jamu, herbal, atau suplemen kesehatan, namun teks promosi mengklaim dapat menyembuhkan penyakit berat tersebut secara mandiri, skor konsistensi medis akan turun drastis (Skor: 15/100).
*   Obat keras modern juga akan dipotong nilainya jika beriklan dengan klaim berlebihan yang melanggar aturan promosi obat resmi (Skor: 30/100).
*   Jika klaim promosi normal dan sesuai dengan kegunaan terdaftar, skor bernilai tinggi (Skor: 95 - 100).

### D. OpenFDA Safety Insight
*   Berdasarkan nama bahan aktif produk yang ditemukan di database BPOM, server mengirimkan permintaan API ke OpenFDA Drug Event Endpoint.
*   Menghitung **Seriousness Ratio** (Jumlah laporan efek samping serius dibagi dengan total laporan kejadian berbahaya untuk zat aktif tersebut).
*   Mengekstrak daftar efek samping yang paling sering dilaporkan oleh pasien secara global (seperti: sakit kepala, mual, diare, pusing) beserta jumlah laporannya.
*   Menyimpan hasil pencarian tersebut di cache database lokal (`adverse_event_cache`) untuk menghemat kuota API dan meningkatkan performa query berikutnya.

### E. Consumer Safety Score Engine
Merupakan algoritma penilai keamanan akhir produk berbasis bobot dengan rumus terpadu:
$$\text{Consumer Safety Score} = (0.25 \times S_{\text{BPOM}}) + (0.35 \times S_{\text{Consistency}}) + (0.25 \times S_{\text{NLP}}) + (0.15 \times S_{\text{FDA}})$$

Dimana:
*   $S_{\text{BPOM}}$: 100 jika produk terdaftar di database BPOM, 0 jika tidak terdaftar.
*   $S_{\text{Consistency}}$: Skor dari Medical Consistency Engine (0-100).
*   $S_{\text{NLP}}$: 100 jika tidak terindikasi overclaim, 50 jika overclaim sedang, 0 jika overclaim tinggi.
*   $S_{\text{FDA}}$: Skor keamanan berdasarkan rasio kejadian serius OpenFDA dan jumlah laporan (maksimum pengurangan 70 poin dari basis nilai 100).

---

## 4. Struktur Output & Laporan Keputusan (Decision Report)

Halaman hasil dirancang agar pengguna dapat memindai status kelayakan produk dalam waktu kurang dari 5 detik dengan urutan elemen visual sebagai berikut:

1.  **Final Verdict (Keputusan Akhir)**: Status keamanan produk paling atas yang ditandai dengan warna yang jelas sesuai dengan tingkat risiko:
    *   🟢 **Aman** (Skor 81 - 100)
    *   🟡 **Cukup Aman** (Skor 61 - 80)
    *   🟠 **Perlu Perhatian** / **Potensi Overclaim** (Skor 31 - 60)
    *   🔴 **Risiko Tinggi** (Skor 0 - 30)
    *   ⚪ **Data Tidak Lengkap**
2.  **AI Executive Summary**: Ringkasan naratif otomatis dalam bahasa Indonesia awam yang menjelaskan mengapa produk mendapat status risiko tersebut berdasarkan kombinasi status BPOM, hasil NLP, dan skor medis.
3.  **Consumer Safety Score**: Tampilan angka skor akhir (0-100) beserta daftar alasan visual (*checklist* hijau untuk tanda positif, *cross* merah untuk penanda negatif).
4.  **Safety Score Breakdown**: Transparansi kontribusi nilai dari masing-masing pilar (BPOM, Konsistensi Medis, NLP, OpenFDA).
5.  **Product Profile**: Tabel identitas produk resmi hasil pencarian database (Nama, No BPOM, Produsen, Kategori, Sediaan, Bahan Aktif, Golongan Terapi, Kode ATC).
6.  **Drug Function (Bahasa Awam)**: Penjelasan fungsi terapi obat dalam kalimat awam (misal: "Membantu menurunkan tekanan darah tinggi" untuk obat golongan hipertensi).
7.  **DDD & Administration Information**: Informasi rute penggunaan (misal: Oral, Transdermal) diterjemahkan ke media penggunaan harian (misal: Diminum, Dioleskan) beserta rujukan dosis harian standar WHO (*Defined Daily Dose* - DDD).
8.  **Evidence (Bukti Analisis)**: Menampilkan kutipan kalimat promosi produk yang ditandai oleh sistem beserta sumbernya.
9.  **Efek Samping Potensial (OpenFDA)**: Daftar efek samping yang sering dilaporkan berdasarkan zat aktif produk disertai jumlah laporan resmi secara global.
10. **Rekomendasi Tindak Lanjut**: Panduan taktis bagi konsumen (misal: instruksi untuk menghindari produk jika risiko tinggi atau saran konsultasi dokter).
11. **Detail Analisis Teknis (Accordion)**: Kontainer tersembunyi untuk audit teknis yang memuat persentase keyakinan model IndoBERT, detail skor konsistensi, visualisasi diagram batang confidence score, dan teks hasil ekstraksi OCR mentah.

---

## 5. Spesifikasi Database (Database Schema)

Database SQLite `waras_id.db` terdiri dari beberapa tabel utama yang saling berelasi:

### A. Tabel `products` (Master Data Produk BPOM)
Menyimpan identitas lengkap produk kesehatan yang terdaftar di BPOM.
*   `id` (INTEGER, Primary Key)
*   `product_name` (TEXT)
*   `registration_number` (TEXT, Indexed) - Nomor registrasi BPOM.
*   `manufacturer` (TEXT) - Produsen pembuat.
*   `product_category` (TEXT) - Kategori (Obat, Suplemen, Jamu, Kosmetik).
*   `ingredient` (TEXT) - Nama zat/bahan aktif penyusun.
*   `atc_code` (TEXT) - Kode Klasifikasi ATC dari WHO.
*   `created_at` / `updated_at` (TIMESTAMP)

### B. Tabel `atc_reference` (Referensi ATC WHO)
Menyimpan informasi dosis harian standar (DDD) dan rute pemberian dari WHO.
*   `atc_code` (TEXT, Primary Key)
*   `atc_name` (TEXT) - Nama resmi zat aktif versi ATC.
*   `ddd` (REAL) - Defined Daily Dose (nilai numerik dosis).
*   `uom` (TEXT) - Unit of Measure (satuan dosis, misal: mg, g, ml).
*   `administration_route` (TEXT) - Kode rute pemberian (O, P, R, TD, dll).
*   `note` (TEXT)

### C. Tabel `atc_hierarchy` (Hierarki ATC)
Menyimpan pohon klasifikasi ATC untuk pemetaan kategori terapi.
*   `code` (TEXT, Primary Key) - Kode level ATC (misal: A, A10, A10B).
*   `name` (TEXT) - Nama kategori terapi.
*   `level` (INTEGER) - Tingkat kedalaman hierarki (1 s.d 5).
*   `parent_code` (TEXT) - Relasi ke kode induk di level atasnya.

### D. Tabel `adverse_event_cache` (Cache Data Efek Samping OpenFDA)
Menyimpan ringkasan efek samping bahan aktif dari OpenFDA untuk menghindari latensi jaringan.
*   `id` (INTEGER, Primary Key)
*   `ingredient_name` (TEXT, Indexed)
*   `adverse_event` (TEXT) - Nama efek samping dalam format JSON (term dan count).
*   `occurrence_count` (INTEGER) - Total laporan kasus kejadian buruk.
*   `severity` (REAL) - Rasio keparahan / kasus serius.
*   `last_updated` (TIMESTAMP)

### E. Tabel `claim_analysis` (Hasil Analisis Klaim NLP)
Menyimpan riwayat teks analisis klaim dan prediksi IndoBERT.
*   `id` (INTEGER, Primary Key)
*   `product_id` (INTEGER, Foreign Key ke `products.id`)
*   `analyzed_text` (TEXT) - Teks yang dianalisis oleh server.
*   `prediction_label` (INTEGER) - Label klasifikasi (0: Normal, 1: Ambigu, 2: Overclaim).
*   `confidence_score` (REAL) - Persentase tingkat keyakinan model.
*   `detected_claims` (TEXT) - Frasa/kata pemicu *overclaim* dalam format JSON.
*   `created_at` (TIMESTAMP)

### F. Tabel `product_analysis` (Hasil Keputusan Akhir)
Menyimpan skor akhir dan rekomendasi hasil analisis produk.
*   `id` (INTEGER, Primary Key)
*   `product_id` (INTEGER, Foreign Key ke `products.id`)
*   `claim_score` (INTEGER) - Skor dari modul NLP.
*   `consistency_score` (INTEGER) - Skor dari Medical Consistency Engine.
*   `safety_score` (INTEGER) - Consumer Safety Score akhir (0-100).
*   `recommendation` (TEXT) - Status keputusan akhir (Aman, Potensi Overclaim, dll).
*   `created_at` (TIMESTAMP)
