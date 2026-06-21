# WARAS-ID

## Output & Decision Report Specification v3.0

---

# Overview

WARAS-ID bukan sekadar sistem NLP untuk mendeteksi overclaim.

WARAS-ID adalah platform analisis produk kesehatan yang menggabungkan:

* BPOM Database
* WHO ATC Database
* OpenFDA Safety Data
* IndoBERT ClaimSense Engine
* Medical Consistency Engine
* Consumer Safety Score Engine

Tujuan utama WARAS-ID adalah memberikan satu keputusan yang mudah dipahami pengguna hanya dari satu kali input.

Input dapat berupa:

* URL Marketplace
* Barcode Produk
* Screenshot Produk
* Nama Produk

Output harus bersifat informatif, transparan, dan mudah dipahami oleh pengguna awam.

---

# Design Principle

Ketika pengguna membuka hasil analisis, mereka harus dapat menjawab pertanyaan berikut dalam waktu kurang dari lima detik:

1. Produk ini apa?
2. Produk ini digunakan untuk apa?
3. Apakah produk ini aman?
4. Apakah ada indikasi overclaim?
5. Mengapa sistem memberikan hasil tersebut?

Output tidak boleh berupa kumpulan angka tanpa penjelasan.

Output harus berbentuk decision report.

---

# Output Structure

Urutan berikut wajib digunakan.

---

# 1. Final Verdict

Bagian paling atas halaman.

Komponen ini merupakan fokus utama seluruh sistem.

Contoh:

## ⚠️ PERLU PERHATIAN

INHITRIL

Lisinopril Dihydrate

Consumer Safety Score: 40 / 100

Produk terdaftar BPOM, namun ditemukan klaim yang tidak sesuai dengan indikasi terapi resmi.

---

Kategori Verdict:

* Aman
* Cukup Aman
* Perlu Perhatian
* Potensi Overclaim
* Risiko Tinggi
* Data Tidak Lengkap

---

Tujuan:

Memberikan jawaban langsung sebelum user membaca detail lainnya.

---

# 2. AI Executive Summary

WARAS-ID wajib menghasilkan ringkasan analisis otomatis.

Contoh:

Produk INHITRIL merupakan obat antihipertensi yang terdaftar di BPOM.

Teks yang dianalisis mengandung klaim bahwa produk dapat menyembuhkan diabetes dan stroke secara permanen tanpa efek samping.

Klaim tersebut tidak sesuai dengan fungsi terapi obat dan mengandung beberapa frasa yang umum ditemukan pada promosi overclaim.

Berdasarkan hasil analisis, sistem memberikan status PERLU PERHATIAN.

---

Tujuan:

* Menjelaskan reasoning sistem
* Membantu pengguna awam
* Membantu juri memahami hasil analisis

---

# 3. Consumer Safety Score

Tampilkan skor akhir secara jelas.

Contoh:

Consumer Safety Score

40 / 100

Kategori:

Perlu Perhatian

---

Wajib menampilkan alasan skor.

Contoh:

Mengapa skor rendah?

✓ Produk terdaftar BPOM

✗ Klaim overclaim terdeteksi

✗ Klaim tidak sesuai indikasi

✗ Mengandung klaim absolut

---

# 4. Consumer Safety Score Breakdown

Jangan hanya menampilkan skor akhir.

Tampilkan sumber kontribusi skor.

Contoh:

BPOM Verification ............. 100

Medical Consistency ........... 30

NLP Claim Analysis ............ 0

OpenFDA Safety Reference ...... 30

Final Score ................... 40

---

Tujuan:

Meningkatkan transparansi.

Mencegah skor terlihat sebagai angka acak.

---

# 5. Product Profile

Menampilkan identitas produk.

Fields:

* Nama Produk
* Nomor Registrasi BPOM
* Produsen
* Kategori Produk
* Bentuk Sediaan
* Zat Aktif
* Golongan Terapi
* Kode ATC

Contoh:

Nama Produk:
INHITRIL

Nomor Registrasi:
DKL123456789

Produsen:
PT XYZ

Kategori:
Obat

Golongan:
ACE Inhibitor

Kode ATC:
C09AA03

---

# 6. Drug Function

Bagian ini menerjemahkan data medis ke bahasa awam.

Jangan hanya menampilkan kode ATC.

Contoh:

Produk ini termasuk obat antihipertensi yang digunakan untuk membantu:

* Menurunkan tekanan darah
* Mengontrol hipertensi
* Mengurangi risiko komplikasi akibat tekanan darah tinggi

---

Tujuan:

Membantu pengguna memahami fungsi produk.

---

# 7. DDD & Administration Information

Bagian ini memanfaatkan data WHO ATC.

Fields:

* DDD
* Satuan
* Administration Route
* Media Penggunaan

Contoh:

DDD:
10 mg

Administration Route:
Oral

Media Penggunaan:
Diminum

---

Contoh lain:

Administration Route:
Topical

Media Penggunaan:
Dioleskan pada kulit

---

Disclaimer wajib:

DDD merupakan standar dosis referensi WHO untuk tujuan klasifikasi dan analisis obat.

DDD bukan petunjuk penggunaan langsung bagi pasien.

---

# 8. Claim Analysis (IndoBERT)

Menampilkan hasil model NLP.

Fields:

* Classification Label
* Confidence Score
* Trigger Words
* Trigger Sentences

Contoh:

Status:
Overclaim

Confidence:
99.8%

Trigger Words:

* ampuh
* permanen
* sembuh total
* tanpa efek samping

---

Jika tidak ditemukan:

Status:
Tidak Terindikasi Overclaim

Confidence:
99.9%

Trigger Words:
Tidak ditemukan

---

# 9. Medical Consistency Analysis

Salah satu fitur utama WARAS-ID.

Tujuan:

Membandingkan:

* Fungsi produk
* Kategori terapi
* Hasil NLP
* Klaim yang ditemukan

---

Contoh:

Medical Consistency Score

30 / 100

Alasan:

✗ Klaim menyembuhkan diabetes

✗ Klaim menyembuhkan stroke

✗ Tidak sesuai fungsi obat hipertensi

✗ Mengandung klaim absolut

---

Contoh lain:

Medical Consistency Score

95 / 100

Alasan:

✓ Klaim sesuai kategori terapi

✓ Tidak ditemukan klaim di luar indikasi

✓ Tidak ditemukan kata absolut

---

Tujuan:

Membuat skor dapat dipahami.

---

# 10. OpenFDA Safety Reference

Digunakan sebagai referensi keamanan berdasarkan zat aktif.

Bukan sebagai penentu utama keamanan produk.

Fields:

* Ingredient Queried
* Total Reports
* Serious Reports
* Common Side Effects

Contoh:

Zat Aktif:

* Lisinopril

Efek Samping yang Sering Dilaporkan:

* Fatigue
* Dizziness
* Headache
* Nausea

---

Disclaimer wajib:

Data OpenFDA berasal dari laporan adverse event global berdasarkan zat aktif.

Data ini tidak menunjukkan bahwa produk tertentu pasti menyebabkan efek samping tersebut.

Informasi digunakan sebagai referensi keamanan tambahan.

---

# 11. Analyzed Text

Menampilkan teks yang dianalisis sistem.

Tujuan:

* Transparansi
* Audit hasil NLP
* Validasi OCR

Contoh:

Teks Dianalisis:

"INHITRIL mampu menyembuhkan diabetes dan stroke secara permanen tanpa efek samping."

---

# 12. Recommendation

Bagian terakhir yang memberikan arahan kepada pengguna.

Contoh Aman:

Produk terdaftar BPOM dan tidak ditemukan indikasi overclaim.

Gunakan sesuai aturan pakai yang tertera pada kemasan.

---

Contoh Perlu Perhatian:

Produk terdaftar BPOM, namun ditemukan klaim yang perlu diperhatikan.

Hindari menjadikan klaim promosi sebagai dasar pengobatan medis.

---

Contoh Overclaim:

Ditemukan indikasi klaim berlebihan yang tidak sesuai dengan fungsi terapi produk.

Sebaiknya lakukan verifikasi tambahan sebelum mempercayai klaim tersebut.

---

# 13. UI Priority

Urutan prioritas visual:

1. Final Verdict
2. AI Executive Summary
3. Consumer Safety Score
4. Product Profile
5. Drug Function
6. DDD & Administration Information
7. Claim Analysis
8. Medical Consistency Analysis
9. OpenFDA Safety Reference
10. Analyzed Text
11. Recommendation

---

# Success Criteria

WARAS-ID dianggap berhasil apabila pengguna dapat:

* Memahami fungsi produk
* Mengetahui status keamanan produk
* Mengetahui potensi overclaim
* Mengetahui alasan keputusan sistem
* Memahami hasil tanpa harus mengerti istilah medis atau AI

Dalam satu kali analisis dan satu halaman hasil.
