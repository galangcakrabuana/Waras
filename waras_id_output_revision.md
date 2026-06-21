# Spesifikasi Revisi Bagian Output WARAS.ID

> Dokumen ini hanya membahas bagian output atau halaman hasil pemeriksaan WARAS.ID.  
> Fokus utama revisi adalah membuat hasil sangat mudah dipahami pengguna awam, tidak terlihat seperti dashboard AI, tidak penuh kartu, serta mampu menjelaskan apa yang ditemukan, mengapa perlu diperhatikan, dan apa yang sebaiknya dilakukan pengguna.

---

# 1. Tujuan Halaman Output

Halaman output harus membantu pengguna menjawab lima pertanyaan:

1. Apa kesimpulan utamanya?
2. Apakah produk ditemukan dalam data resmi?
3. Apakah klaim penjual perlu diperhatikan?
4. Mengapa klaim tersebut dianggap bermasalah?
5. Apa yang sebaiknya dilakukan setelah melihat hasil?

Pengguna tidak boleh dipaksa memahami:

- Label 0, 1, dan 2
- Confidence score
- Risk percentage
- Model prediction
- NLP
- OCR
- IndoBERT
- API response
- Kode ATC mentah
- Istilah teknis backend

Teknologi bekerja di belakang layar. Halaman hasil hanya menampilkan informasi yang membantu pengguna mengambil keputusan.

---

# 2. Prinsip Utama Output

Halaman hasil harus:

- Dimulai dengan kesimpulan
- Menggunakan bahasa sederhana
- Memisahkan status produk dan klaim
- Menampilkan klaim asli yang bermasalah
- Menjelaskan alasan
- Menampilkan informasi resmi
- Memberikan tindakan lanjutan
- Menampilkan sumber dan keterbatasan
- Tetap tenang dan tidak menakut-nakuti
- Mudah dibaca di ponsel

Halaman hasil tidak boleh:

- Berbentuk dashboard
- Menggunakan banyak kartu
- Menggunakan grafik donat
- Menggunakan meter risiko
- Menampilkan angka confidence sebagai fokus
- Menampilkan seluruh output backend
- Menampilkan JSON mentah
- Menampilkan istilah teknis
- Menumpuk banyak badge
- Menggunakan terlalu banyak warna
- Menggunakan animasi yang berlebihan

---

# 3. Struktur Utama Halaman Hasil

Urutan informasi wajib:

1. Tombol kembali atau periksa produk lain
2. Label status utama
3. Kesimpulan
4. Ringkasan alasan
5. Status produk
6. Status klaim penjual
7. Klaim yang perlu diperhatikan
8. Penjelasan alasan
9. Informasi resmi produk
10. Perbandingan klaim dengan manfaat resmi
11. Saran tindakan
12. Sumber data
13. Keterbatasan
14. Disclaimer

Urutan ini tidak boleh dibalik hanya demi desain.

---

# 4. Bagian Paling Atas

Bagian paling atas harus langsung memberi jawaban.

Contoh:

```text
Hasil pemeriksaan

PERLU DIPERHATIKAN

Produk ditemukan dalam data BPOM, tetapi terdapat
klaim promosi yang lebih kuat daripada manfaat resmi
yang ditemukan.
```

Jangan memulai dengan:

```text
Product Intelligence Report
AI Analysis Complete
Confidence 94.7%
Risk Score 72
```

Pengguna ingin kesimpulan, bukan pembukaan seminar model.

---

# 5. Status Utama

Gunakan maksimal empat status publik:

## Tidak ditemukan masalah berarti

```text
TIDAK DITEMUKAN MASALAH BERARTI
```

Makna:

- Produk ditemukan
- Klaim sesuai atau tidak ditemukan klaim berlebihan
- Data cukup untuk pemeriksaan

## Perlu diperhatikan

```text
PERLU DIPERHATIKAN
```

Makna:

- Produk ditemukan
- Ada klaim ambigu, terlalu promosi, atau membutuhkan konteks

## Berisiko tinggi

```text
BERISIKO TINGGI
```

Makna:

- Klaim absolut
- Janji kesembuhan
- Klaim menggantikan pengobatan
- Klaim tanpa efek samping
- Klaim melampaui manfaat resmi

## Belum dapat dipastikan

```text
BELUM DAPAT DIPASTIKAN
```

Makna:

- Data tidak cukup
- OCR tidak jelas
- Produk belum ditemukan
- Informasi klaim terlalu sedikit

Jangan menampilkan status internal model seperti:

```text
0
1
2
safe
ambiguous
overclaim
```

---

# 6. Bentuk Status

Gunakan status label kecil dan jelas.

Rekomendasi visual:

```text
Aman            Hijau
Perhatian       Amber
Berisiko        Merah bata
Tidak pasti     Abu-abu
```

Status tidak boleh hanya ditunjukkan lewat warna.

Wajib ada teks.

Contoh benar:

```text
PERLU DIPERHATIKAN
```

Contoh salah:

```text
Lingkaran kuning tanpa teks
```

---

# 7. Kesimpulan Utama

Kesimpulan harus satu sampai dua kalimat.

Contoh:

```text
Produk ditemukan dalam data BPOM, tetapi terdapat
klaim promosi yang tidak sesuai dengan manfaat resmi.
```

Contoh aman:

```text
Produk ditemukan dalam data BPOM dan tidak ditemukan
klaim berlebihan pada informasi yang berhasil dibaca.
```

Contoh tidak pasti:

```text
Informasi yang tersedia belum cukup untuk memberikan
kesimpulan. Coba unggah gambar yang lebih jelas.
```

Kesimpulan tidak boleh:

- Terlalu panjang
- Berisi jargon
- Menggunakan angka tanpa penjelasan
- Mengandung tuduhan
- Menggunakan bahasa terlalu mutlak

---

# 8. Pisahkan Status Produk dan Klaim

Ini merupakan bagian terpenting.

Tampilkan dua baris utama.

```text
Status produk

Ditemukan dalam data BPOM

Nomor registrasi sesuai dengan nama produk
yang ditemukan.
```

```text
Status klaim penjual

Perlu diperhatikan

Terdapat janji hasil pasti dan batas waktu
yang tidak ditemukan dalam manfaat resmi.
```

Tambahkan penjelasan:

```text
Produk yang terdaftar di BPOM belum tentu dipromosikan
dengan klaim yang tepat oleh penjual.
```

Jangan gabungkan menjadi:

```text
Produk cukup aman
```

Kalimat tersebut terlalu umum dan dapat disalahartikan.

---

# 9. Struktur Status Produk

Status produk dapat berupa:

## Ditemukan

```text
Ditemukan dalam data BPOM
```

Tampilkan:

- Nama resmi
- Nomor registrasi
- Produsen
- Kategori
- Manfaat resmi

## Belum ditemukan

```text
Belum ditemukan dalam data
```

Tambahkan:

```text
Periksa kembali nomor registrasi atau nama produk.
Belum ditemukan bukan berarti produk pasti ilegal.
```

## Data tidak cukup

```text
Data produk belum cukup
```

Tambahkan:

```text
Nama atau nomor registrasi belum terbaca dengan jelas.
```

Jangan gunakan:

```text
Verified
Not verified
Invalid product
Fake product
```

Kecuali benar-benar ada dasar resmi untuk menyatakan itu.

---

# 10. Struktur Status Klaim

Status klaim dapat berupa:

## Tidak ditemukan masalah berarti

```text
Tidak ditemukan klaim berlebihan
```

## Perlu diperhatikan

```text
Terdapat klaim yang membutuhkan konteks
```

## Berisiko tinggi

```text
Terdapat klaim absolut atau janji hasil pasti
```

## Belum dapat dipastikan

```text
Teks klaim belum cukup jelas
```

Jangan tampilkan:

```text
Prediction class: 2
```

---

# 11. Klaim yang Perlu Diperhatikan

Tampilkan kalimat asli yang ditemukan.

Contoh:

```text
“Dijamin menyembuhkan diabetes dalam 7 hari
tanpa efek samping.”
```

Gunakan blockquote atau panel sederhana.

Jangan hanya menampilkan potongan kata tanpa konteks.

Contoh kurang baik:

```text
diabetes
7 hari
tanpa efek samping
```

Pengguna perlu melihat kalimat utuh.

---

# 12. Penjelasan Alasan

Setelah klaim ditampilkan, jelaskan mengapa perlu diperhatikan.

Contoh:

```text
Mengapa perlu diperhatikan?

- “Dijamin menyembuhkan” menjanjikan hasil pasti.
- “Dalam 7 hari” memberikan batas waktu tertentu.
- “Tanpa efek samping” merupakan pernyataan mutlak.
- Klaim tersebut tidak ditemukan dalam manfaat resmi.
```

Jangan menggunakan penjelasan seperti:

```text
Detected by model
High semantic risk
Class probability 0.94
```

Alasan harus berasal dari bahasa pengguna, bukan bahasa model.

---

# 13. Penandaan Bagian Kalimat

Jika memungkinkan, sorot bagian penting.

Contoh:

```text
“Dijamin menyembuhkan” diabetes “dalam 7 hari”
“tanpa efek samping”.
```

Gunakan highlight sederhana.

Jangan terlalu banyak warna.

Gunakan maksimal:

- Amber untuk perhatian
- Merah bata untuk risiko tinggi

Jangan membuat seluruh paragraf berwarna.

---

# 14. Informasi Resmi Produk

Tampilkan dalam format baris.

Contoh:

```text
Nama resmi          Herbal Sehat Plus
Nomor registrasi    TR123456789
Produsen            PT Sehat Nusantara
Kategori             Obat tradisional
Komposisi            ...
```

Gunakan:

- Definition list
- Table sederhana pada desktop
- Stack vertikal pada mobile

Jangan membuat setiap informasi menjadi card.

Jangan menampilkan informasi teknis yang tidak membantu.

---

# 15. Manfaat Resmi

Beri bagian khusus.

Contoh:

```text
Manfaat resmi yang ditemukan

Secara tradisional digunakan untuk membantu
memelihara kondisi tubuh.
```

Bagian ini penting karena menjadi pembanding utama terhadap klaim penjual.

Jangan menyembunyikannya di accordion.

---

# 16. Perbandingan Klaim dan Informasi Resmi

Jika data cukup, tampilkan perbandingan.

Contoh:

```text
Klaim penjual

Menyembuhkan diabetes dalam 7 hari

Informasi resmi

Membantu memelihara kondisi tubuh
```

Pada desktop boleh menggunakan dua kolom.

Pada mobile gunakan urutan vertikal.

Jangan gunakan tabel yang terlalu lebar.

---

# 17. Saran Tindakan

Setiap hasil harus memiliki tindakan yang jelas.

Contoh:

```text
Apa yang sebaiknya dilakukan?

1. Jangan mengganti pengobatan dokter dengan produk ini.
2. Bandingkan klaim penjual dengan manfaat resmi.
3. Periksa kembali informasi pada kemasan.
4. Tanyakan kepada apoteker atau tenaga kesehatan jika ragu.
```

Tindakan harus sesuai dengan status.

---

# 18. Tindakan Berdasarkan Status

## Jika aman

```text
- Tetap gunakan sesuai petunjuk.
- Periksa informasi pada kemasan.
- Konsultasikan jika memiliki kondisi khusus.
```

## Jika perlu diperhatikan

```text
- Jangan langsung percaya pada klaim promosi.
- Bandingkan dengan manfaat resmi.
- Cari sumber tambahan.
```

## Jika berisiko tinggi

```text
- Jangan mengganti pengobatan dokter.
- Hindari klaim hasil pasti.
- Konsultasikan dengan tenaga kesehatan.
```

## Jika belum pasti

```text
- Unggah gambar yang lebih jelas.
- Masukkan nomor BPOM.
- Salin teks klaim secara manual.
```

---

# 19. Tombol pada Halaman Hasil

Gunakan maksimal dua tombol utama.

Contoh:

```text
Lihat dasar pemeriksaan
Periksa produk lain
```

Pilihan tambahan dapat berupa link:

```text
Buka sumber resmi
Laporkan masalah
```

Jangan menampilkan lima atau enam tombol sekaligus.

---

# 20. Sumber Data

Tempatkan di bagian bawah.

Contoh:

```text
Sumber yang digunakan

- Data produk BPOM
- Teks halaman produk
- Informasi pada gambar
- Hasil pemeriksaan klaim WARAS.ID
```

Tambahkan tanggal pembaruan jika tersedia.

Contoh:

```text
Data terakhir diperbarui: 20 Juni 2026
```

Jangan menampilkan daftar endpoint atau nama fungsi backend.

---

# 21. Keterbatasan

Keterbatasan harus terlihat dan mudah dipahami.

Contoh:

```text
Keterbatasan pemeriksaan

- Hasil bergantung pada informasi yang berhasil dibaca.
- Data yang belum ditemukan tidak otomatis berarti produk ilegal.
- Gambar buram dapat menyebabkan teks terbaca tidak lengkap.
- Hasil ini bukan diagnosis atau keputusan medis.
```

Jangan menyembunyikan keterbatasan terlalu dalam.

Gunakan accordion yang tetap mudah ditemukan.

---

# 22. Disclaimer

Gunakan disclaimer singkat.

```text
WARAS.ID adalah alat bantu pemeriksaan awal dan bukan
pengganti diagnosis, konsultasi dokter, atau saran apoteker.
```

Jangan membuat disclaimer sangat panjang hingga tidak dibaca.

---

# 23. Empty State

Jika produk tidak ditemukan:

```text
Produk belum ditemukan dalam data.

Periksa kembali nama atau nomor registrasi.
Belum ditemukan bukan berarti produk pasti ilegal.
```

Tindakan:

```text
Periksa nomor kembali
Unggah foto produk
Buka sumber resmi
```

---

# 24. Uncertain State

Jika hasil belum pasti:

```text
Hasil belum dapat dipastikan.

Informasi produk atau klaim belum cukup jelas.
```

Tambahkan alasan:

```text
- Teks pada gambar terlalu kecil
- Nomor registrasi tidak terbaca
- Deskripsi produk terlalu singkat
```

Tindakan:

```text
Unggah gambar lebih jelas
Masukkan nomor BPOM
Salin teks klaim
```

---

# 25. Error State

Jika terjadi kegagalan teknis:

```text
Hasil belum dapat ditampilkan.

Pemeriksaan belum berhasil diselesaikan.
Coba lagi atau gunakan metode input lain.
```

Tombol:

```text
Coba lagi
Periksa dengan foto
```

Jangan tampilkan:

```text
Internal server error
Model service unavailable
Database timeout
```

---

# 26. Copywriting

## Gunakan

- Hasil pemeriksaan
- Perlu diperhatikan
- Status produk
- Status klaim penjual
- Klaim yang perlu diperhatikan
- Mengapa perlu diperhatikan?
- Informasi resmi produk
- Manfaat resmi
- Apa yang sebaiknya dilakukan?
- Sumber data
- Keterbatasan pemeriksaan

## Hindari

- AI output
- Prediction result
- Confidence
- Risk engine
- NLP score
- Inference completed
- Model result
- Semantic analysis

---

# 27. Nada Bahasa

Nada harus:

- Tenang
- Jelas
- Tidak menghakimi
- Tidak menakut-nakuti
- Tidak terlalu formal
- Tidak sok pintar
- Tidak mutlak

Gunakan:

```text
Klaim ini perlu diperhatikan.
```

Hindari:

```text
Klaim ini bohong.
```

Gunakan:

```text
Produk belum ditemukan.
```

Hindari:

```text
Produk palsu.
```

---

# 28. Struktur Visual

Gunakan section vertikal.

Contoh:

```text
Hasil pemeriksaan

Kesimpulan

────────────────

Status produk
Status klaim

────────────────

Klaim yang perlu diperhatikan

────────────────

Informasi resmi

────────────────

Apa yang sebaiknya dilakukan?

────────────────

Sumber dan keterbatasan
```

Jangan membuat grid card.

---

# 29. Penggunaan Card

Card hanya digunakan untuk:

- Satu klaim penting
- Peringatan khusus
- Informasi yang benar-benar perlu dipisahkan

Jangan membuat card untuk:

- Nama produk
- Nomor registrasi
- Produsen
- Kategori
- Manfaat resmi
- Sumber data
- Setiap rekomendasi

Gunakan border dan spacing.

---

# 30. Visual Status

Status utama dapat menggunakan:

- Label kecil
- Border kiri
- Background lembut
- Teks jelas

Jangan menggunakan:

- Gradient
- Glow
- Animasi pulse
- Meter
- Donut
- Gauge
- Progress bar risiko

Progress bar dapat disalahartikan sebagai probabilitas medis.

---

# 31. Mobile First

Pada mobile:

- Satu kolom
- Kesimpulan muncul paling atas
- Status produk dan klaim ditumpuk
- Informasi resmi dalam baris vertikal
- Tombol selebar container
- Tidak ada tabel lebar
- Tidak ada sticky panel besar
- Font isi minimal 16 px
- Jarak antar section minimal 32 px
- Accordion mudah disentuh

---

# 32. Aksesibilitas

Wajib:

- Heading berurutan
- Status tidak hanya memakai warna
- Fokus tombol terlihat
- Accordion menggunakan `aria-expanded`
- Perubahan hasil diumumkan dengan `aria-live`
- Label status terbaca screen reader
- Kontras warna memadai
- Tombol dapat digunakan keyboard
- Link sumber memiliki nama jelas
- Jangan gunakan ikon tanpa label

---

# 33. Struktur HTML

Contoh:

```html
<section class="result-view" aria-labelledby="result-title">
  <header class="result-header">
    <p>Hasil pemeriksaan</p>
    <span class="status-label">Perlu diperhatikan</span>
    <h1 id="result-title">Beberapa klaim perlu dicermati.</h1>
    <p>...</p>
  </header>

  <section aria-labelledby="status-title">
    <h2 id="status-title">Dua hal yang kami periksa</h2>
    ...
  </section>

  <section aria-labelledby="claim-title">
    <h2 id="claim-title">Klaim yang perlu diperhatikan</h2>
    ...
  </section>

  <section aria-labelledby="official-title">
    <h2 id="official-title">Informasi resmi produk</h2>
    ...
  </section>

  <section aria-labelledby="action-title">
    <h2 id="action-title">Apa yang sebaiknya dilakukan?</h2>
    ...
  </section>
</section>
```

Gunakan HTML semantik.

---

# 34. Struktur CSS

Pisahkan style output.

```text
css/components/
├── result-header.css
├── status-comparison.css
├── claim-review.css
├── official-info.css
├── recommendation.css
├── source-details.css
└── result-state.css
```

Gunakan penamaan konsisten.

```text
result-view
result-header
result-section
status-row
claim-item
product-facts
recommendation-list
result-details
```

---

# 35. Struktur JavaScript

Pisahkan:

```text
js/
├── renderers/
│   ├── result-renderer.js
│   ├── claim-renderer.js
│   ├── product-renderer.js
│   ├── recommendation-renderer.js
│   └── error-renderer.js
├── mappers/
│   └── result-view-model.js
└── controllers/
    └── result-controller.js
```

Jangan membuat satu fungsi render dengan ratusan baris.

---

# 36. View Model

Frontend harus menerima data yang sudah siap ditampilkan.

Contoh:

```js
{
  status: "attention",
  statusLabel: "Perlu diperhatikan",
  title: "Beberapa klaim perlu dicermati.",
  summary: "Produk ditemukan, tetapi...",
  product: {
    registrationStatus: "found",
    registrationLabel: "Ditemukan dalam data BPOM",
    name: "Herbal Sehat Plus",
    registrationNumber: "TR123456789",
    manufacturer: "PT Sehat Nusantara",
    category: "Obat tradisional",
    officialBenefit: "..."
  },
  claimAnalysis: {
    status: "high",
    label: "Berisiko tinggi",
    summary: "...",
    claims: [
      {
        text: "...",
        reasons: []
      }
    ]
  },
  recommendations: [],
  sources: [],
  limitations: []
}
```

Jangan menghubungkan UI langsung ke output mentah model.

---

# 37. Keamanan Rendering

Wajib:

- Gunakan `textContent`
- Hindari `innerHTML` untuk data pengguna
- Sanitasi data dari backend
- Jangan render URL tanpa validasi
- Jangan render stack trace
- Jangan tampilkan prompt internal
- Jangan tampilkan confidence mentah
- Jangan tampilkan response JSON

---

# 38. Hal yang Harus Dihapus dari Output Lama

Hapus:

- Dashboard
- Sidebar
- Banyak card
- Grafik donat
- Risk meter
- Confidence score
- Emoji
- Badge berlebihan
- Gradient
- Shadow tebal
- Tab teknis
- Label angka
- JSON mentah
- Output model
- Istilah AI
- Statistik yang tidak berguna
- CTA terlalu banyak

---

# 39. Hal yang Harus Dipertahankan

Pertahankan:

- Status produk
- Status klaim
- Klaim yang ditemukan
- Informasi resmi
- Manfaat resmi
- Rekomendasi
- Sumber data
- Disclaimer

Pertahankan informasi penting, tetapi ubah cara penyampaiannya.

---

# 40. Checklist Output

## Struktur

- [ ] Kesimpulan muncul pertama
- [ ] Status produk terpisah
- [ ] Status klaim terpisah
- [ ] Klaim asli ditampilkan
- [ ] Alasan ditampilkan
- [ ] Informasi resmi ditampilkan
- [ ] Rekomendasi ditampilkan
- [ ] Sumber dan keterbatasan tersedia

## Pemahaman

- [ ] Tidak ada jargon teknis
- [ ] Tidak ada label angka
- [ ] Tidak ada confidence score
- [ ] Bahasa sederhana
- [ ] Tindakan jelas
- [ ] Tidak menghakimi

## Visual

- [ ] Tidak menggunakan dashboard
- [ ] Tidak menggunakan grafik risiko
- [ ] Tidak menggunakan card berlebihan
- [ ] Tidak menggunakan gradient
- [ ] Tidak menggunakan emoji
- [ ] Status dapat dipahami tanpa warna
- [ ] Mobile rapi

## State

- [ ] Success
- [ ] Safe
- [ ] Attention
- [ ] High risk
- [ ] Empty
- [ ] Uncertain
- [ ] Error

## Kode

- [ ] Renderer terpisah
- [ ] Mapper terpisah
- [ ] Tidak menggunakan innerHTML untuk data pengguna
- [ ] Tidak menampilkan response mentah
- [ ] Struktur HTML semantik
- [ ] CSS terpisah
- [ ] State terdokumentasi

---

# 41. Instruksi untuk Coding Agent

1. Fokus hanya pada bagian output.
2. Jangan mengubah bagian input.
3. Jangan merusak backend.
4. Rombak hasil menjadi laporan vertikal.
5. Hapus dashboard.
6. Hapus grafik risiko.
7. Hapus confidence score.
8. Pisahkan status produk dan klaim.
9. Tampilkan klaim asli.
10. Tampilkan alasan.
11. Tampilkan manfaat resmi.
12. Tambahkan tindakan lanjutan.
13. Tambahkan sumber.
14. Tambahkan keterbatasan.
15. Gunakan bahasa awam.
16. Pastikan mobile-first.
17. Gunakan HTML semantik.
18. Pisahkan renderer.
19. Gunakan view model.
20. Dokumentasikan file yang diubah.

---

# 42. Kriteria Selesai

Output dianggap selesai jika pengguna dapat:

1. Memahami kesimpulan dalam beberapa detik.
2. Membedakan status produk dan klaim.
3. Mengetahui kalimat yang bermasalah.
4. Mengetahui alasan peringatan.
5. Melihat manfaat resmi.
6. Mengetahui tindakan berikutnya.
7. Mengetahui sumber data.
8. Memahami keterbatasan sistem.

Hasil akhir harus terasa:

- Jelas
- Tenang
- Kredibel
- Tidak ramai
- Tidak teknis
- Tidak menghakimi
- Tidak seperti dashboard
- Sesuai dengan WARAS.ID

---

# 43. Contoh Output Akhir

```text
← Periksa produk lain

Hasil pemeriksaan

PERLU DIPERHATIKAN

Produk ditemukan dalam data BPOM, tetapi terdapat
klaim promosi yang lebih kuat daripada manfaat resmi.

────────────────

Dua hal yang kami periksa

Status produk
Ditemukan dalam data BPOM

Status klaim penjual
Berisiko tinggi

Produk yang terdaftar di BPOM belum tentu dipromosikan
dengan klaim yang tepat oleh penjual.

────────────────

Klaim yang perlu diperhatikan

“Dijamin menyembuhkan diabetes dalam 7 hari
tanpa efek samping.”

Mengapa perlu diperhatikan?

- Menjanjikan kesembuhan pasti.
- Memberikan batas waktu.
- Menggunakan pernyataan tanpa efek samping.
- Tidak sesuai dengan manfaat resmi.

────────────────

Informasi resmi produk

Nama resmi          Herbal Sehat Plus
Nomor registrasi    TR123456789
Produsen            PT Sehat Nusantara
Kategori             Obat tradisional

Manfaat resmi

Secara tradisional digunakan untuk membantu
memelihara kondisi tubuh.

────────────────

Apa yang sebaiknya dilakukan?

1. Jangan mengganti pengobatan dokter.
2. Bandingkan klaim dengan manfaat resmi.
3. Tanyakan kepada tenaga kesehatan jika ragu.

[ Lihat dasar pemeriksaan ]
[ Periksa produk lain ]

────────────────

Sumber data dan keterbatasan
```

---

# 44. Kesimpulan

Output WARAS.ID harus membuat pengguna merasa:

> Saya langsung tahu hasilnya, saya mengerti alasannya, dan saya tahu apa yang harus dilakukan.

Bukan:

> Saya melihat banyak skor, grafik, badge, dan istilah teknis tetapi tetap tidak tahu apakah klaimnya masuk akal.

Output yang baik bukan output yang terlihat canggih.

Output yang baik adalah output yang membuat pengguna paham.
