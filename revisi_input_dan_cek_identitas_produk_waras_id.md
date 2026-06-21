# Spesifikasi Revisi Halaman Input dan Penambahan Fitur Cek Identitas Produk WARAS.ID

## 1. Ringkasan Tugas

Lakukan revisi pada sisi input WARAS.ID tanpa mengurangi fitur yang sudah tersedia.

Revisi harus berfokus pada:

1. Menyederhanakan halaman input agar tugas utama pengguna lebih cepat terlihat.
2. Mengurangi tampilan yang terasa seperti template SaaS atau hasil generasi otomatis.
3. Mempertahankan empat metode pemeriksaan yang sudah ada:
   - Link produk
   - Foto barcode
   - Screenshot atau gambar iklan
   - Teks klaim
4. Menambahkan fitur **Cek Identitas Produk** tanpa menjadikannya metode input kelima.
5. Menjaga seluruh integrasi, ID elemen, event listener, payload request, dan endpoint backend yang sudah berjalan.
6. Membuat pengalaman penggunaan yang mudah dipahami oleh pengguna awam.

Fokus pekerjaan ini adalah halaman input atau home page. Jangan merombak halaman hasil utama di luar kebutuhan integrasi fitur Cek Identitas Produk.

---

## 2. Konteks Produk

WARAS.ID adalah layanan pemeriksaan awal produk kesehatan.

Pengguna dapat memasukkan informasi produk melalui link marketplace, foto barcode, screenshot iklan, atau teks klaim. Sistem kemudian membantu pengguna memahami:

- Risiko klaim produk
- Alasan suatu klaim ditandai
- Informasi registrasi BPOM
- Informasi bahan aktif dan kategori terapi
- Saran langkah berikutnya
- Informasi keamanan pendukung

WARAS.ID ditujukan untuk pengguna awam. Antarmuka harus mengutamakan kejelasan, ketenangan, dan kepercayaan, bukan menonjolkan kecanggihan teknis sistem.

---

## 3. Tujuan Revisi

### 3.1 Tujuan utama

Halaman input harus membuat pengguna memahami tiga hal dalam beberapa detik:

1. Apa yang dapat diperiksa oleh WARAS.ID.
2. Apa yang perlu dimasukkan.
3. Tombol mana yang harus ditekan untuk memulai.

### 3.2 Sasaran pengalaman pengguna

Setelah revisi:

- Form pemeriksaan utama harus terlihat lebih cepat.
- Pengguna tidak perlu melewati terlalu banyak penjelasan sebelum mengisi data.
- Pengguna dapat membedakan pemeriksaan klaim dengan pemeriksaan identitas produk.
- Pengguna tidak bingung membedakan tujuan pemeriksaan dan metode input.
- Seluruh fitur lama tetap tersedia dan berfungsi.

---

## 4. Prinsip Desain

Gunakan prinsip berikut selama revisi:

- Sederhana dan mudah dipindai.
- Tenang dan kredibel.
- Berorientasi pada pengguna awam.
- Tidak terasa seperti dashboard admin.
- Tidak terasa seperti landing page startup generik.
- Tidak menampilkan seluruh fitur dalam bentuk card.
- Tidak menggunakan dekorasi yang tidak membantu tugas pengguna.
- Menggunakan ruang kosong, tipografi, dan garis pemisah secara hemat.
- Menggunakan satu warna aksen utama.
- Memprioritaskan keterbacaan daripada efek visual.

### 4.1 Hindari

- Gradient
- Glassmorphism
- Glow
- Shadow besar
- Card di dalam card
- Radius terlalu besar
- Badge berlebihan
- Emoji
- Ikon dekoratif tanpa fungsi
- Animasi yang menghambat
- Terlalu banyak garis horizontal
- Terlalu banyak teks sebelum form
- Istilah teknis pada alur utama

---

## 5. Arsitektur Informasi yang Direkomendasikan

Gunakan urutan halaman berikut:

```text
Navbar

Hero singkat
- Eyebrow
- Judul utama
- Deskripsi singkat
- Tombol menuju form
- Penjelasan singkat isi hasil

Area pemeriksaan utama
- Pilihan tujuan pemeriksaan
- Pilihan metode input
- Panel input aktif
- Status atau pesan kesalahan

Cara kerja
- Pilih sumber
- Masukkan informasi
- Baca hasil

Yang diperiksa
- BPOM
- Klaim produk
- Saran sederhana

Disclaimer
```

Form utama harus muncul sebelum bagian cara kerja dan informasi pendukung.

---

## 6. Revisi Hero

### 6.1 Struktur hero

Hero cukup memuat:

- Satu eyebrow
- Satu H1
- Satu paragraf pendek
- Satu tombol utama
- Satu keterangan singkat mengenai isi hasil

Jangan gunakan side note atau card tambahan di dalam hero.

### 6.2 Rekomendasi copy

Eyebrow:

```text
PEMERIKSA KLAIM PRODUK KESEHATAN
```

Judul:

```text
Cek klaim produk kesehatan dengan lebih mudah.
```

Deskripsi:

```text
Masukkan link, foto barcode, gambar iklan, atau teks klaim. WARAS.ID membantu menemukan informasi penting sebelum kamu membeli atau menggunakan produk.
```

Tombol:

```text
Mulai periksa produk
```

Keterangan hasil:

```text
Hasil mencakup risiko klaim, alasan utama, informasi BPOM, dan saran sederhana.
```

### 6.3 Aturan tata letak

- Jangan membuat hero terlalu tinggi.
- Kurangi padding atas dan bawah.
- Pada desktop, judul maksimal sekitar dua baris.
- Pada mobile, tombol harus memenuhi lebar container.
- Keterangan hasil dapat berada di bawah tombol.
- Hindari menempatkan tombol dan paragraf panjang dalam satu baris sempit.

---

## 7. Penempatan Alur Tiga Langkah

Pindahkan alur tiga langkah ke bawah panel input.

Gunakan tampilan sederhana:

```text
1. Pilih sumber
2. Masukkan informasi
3. Baca hasil pemeriksaan
```

Pada desktop, langkah dapat ditampilkan horizontal.

Pada mobile, langkah dapat ditampilkan vertikal.

Jangan menggunakan tiga card terpisah. Gunakan nomor kecil, teks, dan pemisah sederhana.

---

## 8. Pilihan Tujuan Pemeriksaan

Tambahkan pilihan tujuan sebelum pilihan metode input.

Pilihan tujuan:

```text
Apa yang ingin kamu lakukan?

[ Periksa klaim produk ] [ Cek identitas produk ]
```

### 8.1 Periksa Klaim Produk

Ini adalah mode default.

Mode ini mempertahankan seluruh metode input lama:

- Link produk
- Foto barcode
- Screenshot atau gambar iklan
- Teks klaim

### 8.2 Cek Identitas Produk

Mode ini digunakan saat pengguna hanya ingin memastikan bahwa identitas produk sesuai dengan data yang tersedia.

Fitur ini bukan metode input kelima. Fitur ini adalah tujuan pemeriksaan yang berbeda.

### 8.3 Bentuk komponen

Gunakan segmented control atau dua tombol pilihan sederhana.

Jangan membuat dua card besar.

Gunakan label yang jelas dan state aktif yang terlihat melalui:

- Ketebalan teks
- Warna teks
- Garis bawah atau border sederhana
- `aria-selected`

Jangan hanya mengandalkan warna.

---

## 9. Revisi Pilihan Metode Input

Pada mode **Periksa Klaim Produk**, tampilkan tab:

```text
Link Produk
Foto Barcode
Gambar Iklan
Teks Klaim
```

### 9.1 Aturan tab

- Semua tab memiliki tinggi yang sama.
- Jangan menggunakan card besar.
- Hanya metode aktif yang menampilkan penjelasan lengkap.
- Metode tidak aktif cukup menampilkan nama.
- Label “Direkomendasikan” untuk Link Produk dipindahkan ke panel aktif atau dibuat sangat ringkas.
- Jangan membuat badge yang mengganggu alignment tab.
- Pastikan tab dapat digunakan dengan keyboard.
- Gunakan `role="tablist"`, `role="tab"`, `aria-selected`, dan `aria-controls`.

### 9.2 Responsiveness

Pada mobile:

- Tab dapat menggunakan horizontal scroll.
- Alternatifnya, gunakan dua kolom.
- Jangan memotong teks.
- Pastikan area sentuh cukup besar.

---

## 10. Panel Link Produk

Pertahankan fungsi input link yang sudah ada.

### 10.1 Struktur

```text
Link Produk
Cara yang disarankan

Tempel link produk yang ingin diperiksa
[ Input link produk ]
[ Periksa produk ]

Gunakan link halaman produk, bukan halaman pencarian atau keranjang.
```

### 10.2 Ketentuan

- Tambahkan `<label>` yang terhubung dengan input.
- Jangan hanya mengandalkan placeholder.
- Pada desktop, input dan tombol dapat sejajar.
- Pada mobile, tombol berada di bawah input dan memenuhi lebar container.
- Pertahankan ID input dan selector JavaScript yang sudah digunakan.
- Validasi link harus memberikan pesan yang spesifik.
- Jangan mengubah format payload atau endpoint.

### 10.3 State kesalahan

Contoh:

```text
Link belum dapat diperiksa.
Pastikan kamu menyalin link halaman produk, bukan halaman pencarian atau keranjang.
```

---

## 11. Panel Foto Barcode

Pertahankan:

- Drag and drop
- Pilihan file dari perangkat
- Preview atau status file
- Proses pembacaan barcode
- Tombol pemeriksaan yang sudah terhubung ke sistem

### 11.1 Struktur

```text
Foto barcode produk

Unggah foto barcode dari kemasan.
Pastikan kode terlihat jelas dan tidak terpotong.

[ Area unggah ]

Nama file
Ukuran file
[ Ganti foto ] [ Hapus ]

[ Periksa produk ]
```

### 11.2 Ketentuan

- Area unggah tidak perlu dibuat seperti card dekoratif.
- Gunakan border sederhana.
- Tampilkan state drag-over yang jelas.
- Area harus dapat diaktifkan dengan keyboard.
- Tambahkan batas ukuran dan format file jika backend memilikinya.
- Jangan mengubah proses upload yang sudah ada.

### 11.3 State gagal

```text
Barcode belum berhasil dibaca.

Coba foto ulang dengan cahaya lebih terang atau gunakan metode lain:
[ Gambar iklan ] [ Teks klaim ]
```

---

## 12. Panel Gambar Iklan

Ganti istilah utama “Screenshot” menjadi **Gambar Iklan** agar lebih mudah dipahami pengguna awam.

Istilah screenshot tetap dapat disebut pada deskripsi.

### 12.1 Struktur

```text
Gambar iklan atau promosi

Unggah screenshot, poster, atau gambar promosi yang ingin diperiksa.

[ Area unggah ]

Nama file
Ukuran file
[ Ganti gambar ] [ Hapus ]

[ Periksa gambar ]
```

### 12.2 Ketentuan

- Pertahankan OCR.
- Jangan mengubah endpoint OCR.
- Pertahankan drag and drop.
- Berikan petunjuk bahwa gambar harus jelas.
- Tampilkan hasil pemilihan file sebelum proses dimulai.

### 12.3 State gagal

```text
Teks pada gambar belum dapat dibaca.

Gunakan gambar yang lebih jelas atau salin kalimat promosi ke metode Teks Klaim.
```

---

## 13. Panel Teks Klaim

### 13.1 Struktur

```text
Teks klaim produk

Salin kalimat promosi, caption, atau pesan penjual yang ingin diperiksa.

[ Textarea ]

0 / batas karakter

[ Periksa teks ]
```

### 13.2 Ketentuan

- Tambahkan label textarea.
- Pertahankan contoh pada placeholder.
- Textarea tidak boleh terlalu pendek.
- Tambahkan penghitung karakter bila tidak mengganggu logika.
- Jangan mengubah format request yang sudah ada.
- Tombol pemeriksaan harus terlihat sebagai aksi utama.

### 13.3 Contoh placeholder

```text
Contoh: Produk ini diklaim dapat menyembuhkan diabetes secara permanen dalam 30 hari.
```

---

## 14. Fitur Cek Identitas Produk

## 14.1 Tujuan fitur

Fitur ini digunakan untuk membantu pengguna memastikan kecocokan identitas produk dengan data yang tersedia.

Fitur harus membantu menjawab:

- Apakah produk ditemukan?
- Apakah nama produk sesuai?
- Apakah nomor registrasi sesuai?
- Siapa produsennya?
- Apa kategori produknya?
- Apa bahan aktifnya?
- Apakah data yang dimasukkan cocok dengan data referensi?

Fitur ini tidak menyatakan bahwa produk pasti aman hanya karena ditemukan di database.

---

## 14.2 Istilah yang digunakan

Gunakan:

```text
Cek Identitas Produk
```

Jangan gunakan “Cek Identitas Obat” sebagai istilah utama karena sistem dapat mencakup produk kesehatan lain.

Deskripsi:

```text
Pastikan nama, nomor BPOM, produsen, dan informasi produk sesuai dengan data yang tersedia.
```

---

## 14.3 Metode pencarian identitas

Pada mode Cek Identitas Produk, sediakan dua cara:

### Cara utama

Satu kolom pencarian:

```text
Nama produk atau nomor BPOM
```

Placeholder:

```text
Contoh: Paracetamol 500 mg atau DKL1234567890A1
```

Tombol:

```text
Cari produk
```

### Cara alternatif

Unggah foto barcode:

```text
Atau gunakan foto barcode dari kemasan
```

Gunakan komponen upload yang sama dengan panel barcode bila memungkinkan.

Jangan menduplikasi logika upload. Gunakan fungsi, komponen, dan handler yang dapat digunakan kembali.

---

## 14.4 Hasil Cek Identitas Produk

Hasil awal harus sederhana dan mudah dibaca.

### Produk ditemukan

```text
Produk ditemukan

Nama produk
Nomor registrasi
Kategori produk
Produsen
Bahan aktif
Status kecocokan data
```

### Produk tidak ditemukan

```text
Produk belum ditemukan

Periksa kembali ejaan nama atau nomor BPOM. Kamu juga dapat mencoba menggunakan foto barcode.
```

### Data cocok sebagian

```text
Sebagian informasi cocok

Nomor registrasi ditemukan, tetapi nama atau produsen yang dimasukkan tidak sepenuhnya sesuai. Periksa kembali kemasan produk.
```

### Sistem tidak dapat mengakses sumber data

```text
Data identitas belum dapat diperiksa

Layanan sumber data sedang tidak tersedia. Coba beberapa saat lagi.
```

---

## 14.5 Status kecocokan

Gunakan status berikut:

- Sesuai
- Cocok sebagian
- Tidak ditemukan
- Belum dapat diverifikasi

Jangan menggunakan istilah “aman” hanya berdasarkan validasi identitas.

Tambahkan penjelasan:

```text
Produk yang ditemukan dalam database belum tentu memiliki klaim promosi yang benar. Gunakan pemeriksaan klaim untuk menilai isi iklan atau deskripsinya.
```

Sediakan aksi lanjutan:

```text
[ Periksa klaim produk ini ]
```

Aksi tersebut harus mengarahkan pengguna kembali ke mode Periksa Klaim Produk dengan data yang sudah tersedia bila memungkinkan.

---

## 15. Bagian “Yang Diperiksa”

Pertahankan informasi:

- BPOM
- Klaim produk
- Saran sederhana

Jangan tampilkan sebagai tiga card besar.

Gunakan satu section sederhana dengan tiga kolom atau daftar horizontal.

Contoh:

```text
Yang diperiksa

BPOM
Mencari kecocokan nomor registrasi dan identitas produk.

Klaim produk
Menandai kalimat yang terdengar terlalu menjanjikan.

Saran sederhana
Memberi ringkasan langkah berikutnya dalam bahasa awam.
```

Pada mobile, ubah menjadi susunan vertikal.

---

## 16. Disclaimer

Pertahankan disclaimer sebagai satu blok sederhana.

Copy yang direkomendasikan:

```text
WARAS.ID membantu melakukan pemeriksaan awal. Hasilnya bukan pengganti konsultasi dokter, apoteker, atau keputusan resmi otoritas kesehatan.
```

Untuk fitur identitas, tambahkan:

```text
Kecocokan identitas produk tidak otomatis membuktikan bahwa seluruh klaim promosi produk benar.
```

Jangan gunakan warna peringatan yang terlalu agresif.

---

## 17. Loading, Empty, Success, dan Error State

Setiap alur harus memiliki state yang jelas.

### 17.1 Loading

Gunakan copy spesifik berdasarkan proses:

```text
Sedang membaca informasi produk...
Sedang memeriksa identitas produk...
Sedang membaca teks pada gambar...
Sedang menganalisis klaim...
```

Loading overlay harus memiliki:

```html
role="status"
aria-live="polite"
aria-hidden="true"
```

Pastikan `aria-hidden` diperbarui ketika loading aktif atau tidak aktif.

### 17.2 Empty state

Jangan mengizinkan pemeriksaan dengan data kosong.

Gunakan pesan spesifik:

```text
Masukkan link produk terlebih dahulu.
Pilih foto barcode terlebih dahulu.
Unggah gambar iklan terlebih dahulu.
Masukkan teks klaim terlebih dahulu.
Masukkan nama atau nomor BPOM terlebih dahulu.
```

### 17.3 Error state

Jangan hanya menampilkan:

```text
Terjadi kesalahan.
```

Jelaskan masalah dan langkah yang dapat dilakukan pengguna.

### 17.4 Partial result

Jika sebagian sumber data gagal, tetap tampilkan hasil yang tersedia.

Contoh:

```text
Analisis klaim berhasil, tetapi data identitas produk belum dapat dimuat.
```

Jangan menghapus seluruh hasil hanya karena satu integrasi gagal.

---

## 18. Aksesibilitas

Pastikan:

- Semua input memiliki label.
- Semua tombol non-submit memiliki `type="button"`.
- Tab dapat dipilih dengan keyboard.
- Focus state terlihat jelas.
- Area upload dapat diaktifkan dengan Enter atau Space.
- Status file diumumkan dengan `aria-live`.
- Loading diumumkan dengan `aria-live`.
- State aktif tidak hanya ditunjukkan dengan warna.
- Kontras teks memadai.
- Ukuran teks utama minimal 16px.
- Area sentuh tombol cukup besar.
- Tidak ada teks yang hanya dapat dipahami melalui ikon.

---

## 19. Responsiveness

Uji minimal pada:

- 375px
- 768px
- 1024px
- 1440px

### 19.1 Mobile

- Tombol aksi utama memenuhi lebar container.
- Input dan tombol ditumpuk.
- Tab tidak terpotong.
- Hero lebih ringkas.
- Tidak ada overflow horizontal.
- Area upload mudah disentuh.
- Teks bantuan tidak terlalu kecil.

### 19.2 Tablet

- Pastikan form utama terlihat lebih cepat.
- Kurangi jarak vertikal berlebihan.
- Hindari terlalu banyak garis pemisah.
- Tab harus tetap terbaca.

### 19.3 Desktop

- Batasi lebar konten agar baris teks tidak terlalu panjang.
- Jangan membuat komponen terlalu melebar.
- Gunakan whitespace secara proporsional.

---

## 20. Struktur Kode

### 20.1 Pemisahan file

Pertahankan:

```text
HTML
CSS
JavaScript
```

Jangan menambahkan:

- Inline CSS
- Inline JavaScript
- Framework baru
- Dependency baru tanpa kebutuhan yang jelas

### 20.2 Class semantik

Gunakan nama class berdasarkan fungsi.

Contoh:

```text
hero
hero-actions
check-purpose
check-purpose-option
check-method-tabs
check-method-tab
check-panel
form-field
upload-area
upload-status
input-helper
process-steps
trust-section
disclaimer
identity-search
identity-result
status-message
```

Ganti class generik seperti `u-style-*` pada bagian input yang direvisi.

### 20.3 ID dan JavaScript

Sebelum mengganti struktur HTML:

1. Periksa seluruh selector JavaScript.
2. Identifikasi ID yang digunakan event listener.
3. Pertahankan ID lama bila memungkinkan.
4. Jika ID harus diubah, perbarui seluruh referensinya.
5. Pastikan tidak ada event listener ganda.
6. Pastikan pergantian mode tidak menghapus nilai input tanpa alasan.
7. Gunakan fungsi reusable untuk upload dan validasi.

---

## 21. Integrasi Backend

Jangan mengubah:

- Endpoint pemeriksaan klaim
- Payload request lama
- Cara backend menerima link
- Cara backend menerima file
- Cara backend menerima teks
- Model NLP
- OCR
- Struktur respons lama

Untuk fitur Cek Identitas Produk:

1. Periksa apakah endpoint pencarian produk sudah tersedia.
2. Jika tersedia, gunakan endpoint tersebut.
3. Jika belum tersedia, buat kontrak endpoint baru secara terpisah.
4. Jangan mencampur respons pencarian identitas dengan respons analisis klaim tanpa alasan.
5. Gunakan error handling, timeout, dan loading state.
6. Hindari request otomatis pada setiap karakter.
7. Gunakan tombol pencarian atau debounce yang wajar bila pencarian langsung memang diperlukan.

Contoh kontrak endpoint yang direkomendasikan:

```http
GET /api/products/search?q={name_or_registration}
```

atau:

```http
POST /api/products/identity-check
Content-Type: application/json
```

Contoh payload:

```json
{
  "query": "DKL1234567890A1"
}
```

Untuk barcode:

```http
POST /api/products/identity-check/barcode
Content-Type: multipart/form-data
```

Jangan menerapkan kontrak baru sebelum memeriksa struktur backend yang sudah ada.

---

## 22. Batas Pekerjaan

Jangan:

- Menghapus salah satu metode input.
- Menjadikan Cek Identitas Produk sebagai tab metode kelima.
- Mengubah halaman hasil klaim secara total.
- Mengubah endpoint lama.
- Mengubah payload lama.
- Mengubah model ClaimSense.
- Mengubah proses OCR tanpa kebutuhan.
- Membuat ulang project dari nol.
- Menambahkan login.
- Menambahkan dashboard admin.
- Menambahkan fitur rekomendasi produk.
- Menyatakan produk aman hanya karena terdaftar.
- Menambahkan animasi berlebihan.
- Menggunakan data dummy pada production flow.

---

## 23. Tahapan Implementasi

### Tahap 1: Audit

- Baca HTML, CSS, dan JavaScript terkait halaman input.
- Identifikasi seluruh selector dan ID.
- Identifikasi endpoint yang digunakan.
- Identifikasi state loading dan error.
- Jelaskan file yang akan diubah.

### Tahap 2: Restrukturisasi halaman input

- Ringkas hero.
- Pindahkan form lebih dekat ke atas.
- Pindahkan langkah ke bawah form.
- Ubah metode input menjadi tab ringkas.
- Pertahankan seluruh fungsi lama.

### Tahap 3: Tambahkan pilihan tujuan

- Tambahkan mode Periksa Klaim Produk.
- Tambahkan mode Cek Identitas Produk.
- Pastikan mode default adalah Periksa Klaim Produk.
- Pastikan switching tidak merusak input lama.

### Tahap 4: Implementasikan Cek Identitas Produk

- Tambahkan pencarian nama atau nomor BPOM.
- Tambahkan alternatif foto barcode.
- Hubungkan ke backend yang tersedia.
- Tambahkan loading, success, partial, empty, dan error state.

### Tahap 5: Refactor dan aksesibilitas

- Ganti class generik pada sisi input.
- Hapus CSS input yang tidak digunakan.
- Tambahkan label, ARIA, dan keyboard interaction.
- Pastikan tidak ada inline style baru.

### Tahap 6: Pengujian

- Uji seluruh metode lama.
- Uji mode identitas.
- Uji tampilan responsif.
- Uji error state.
- Periksa console.
- Pastikan tidak ada regression.

---

## 24. Acceptance Criteria

Pekerjaan dianggap selesai jika:

### Pemeriksaan klaim

- Link produk tetap dapat diperiksa.
- Foto barcode tetap dapat diunggah.
- Drag and drop barcode tetap bekerja.
- Gambar iklan tetap dapat diunggah.
- OCR tetap berjalan.
- Teks klaim tetap dapat diperiksa.
- Loading overlay tetap bekerja.
- Navigasi ke hasil tetap bekerja.
- Tidak ada perubahan pada payload lama.

### Cek identitas produk

- Pengguna dapat memilih Cek Identitas Produk.
- Pengguna dapat mencari berdasarkan nama atau nomor BPOM.
- Pengguna dapat menggunakan foto barcode.
- Produk ditemukan menampilkan identitas utama.
- Produk tidak ditemukan memiliki pesan dan solusi.
- Status kecocokan tidak menggunakan kata “aman”.
- Tersedia aksi untuk melanjutkan ke pemeriksaan klaim.

### UI dan UX

- Form utama terlihat lebih cepat.
- Tidak ada empat card metode besar.
- Tidak ada card di dalam card.
- Hero lebih ringkas.
- Alur tiga langkah berada di bawah form.
- Tidak ada overflow pada mobile.
- Tab dapat digunakan dengan keyboard.
- Semua input memiliki label.
- Tidak ada error JavaScript di console.

### Kode

- HTML, CSS, dan JavaScript tetap terpisah.
- Tidak ada dependency baru yang tidak diperlukan.
- Class baru menggunakan nama semantik.
- CSS lama yang tidak terpakai sudah dibersihkan.
- Fungsi upload tidak diduplikasi secara tidak perlu.
- Perubahan dijelaskan setelah implementasi.

---

## 25. Instruksi Akhir untuk Agen

Sebelum mulai coding:

1. Baca seluruh struktur repository.
2. Baca file HTML, CSS, dan JavaScript halaman input.
3. Cari seluruh penggunaan ID, class, endpoint, dan event listener yang terkait.
4. Jelaskan singkat rencana dan file yang akan diubah.
5. Jangan mengubah halaman hasil atau backend lama tanpa kebutuhan yang jelas.

Setelah itu, implementasikan revisi langsung pada kode yang ada.

Jangan membuat mockup terpisah.

Jangan menghapus fitur.

Jangan membuat project baru.

Setelah selesai, laporkan:

- File yang diubah
- Perubahan struktur UI
- Perubahan JavaScript
- Integrasi fitur identitas
- Pengujian yang dilakukan
- Kendala atau asumsi yang masih tersisa
