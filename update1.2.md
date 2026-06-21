Tolong revisi total UI/UX sisi input WARAS.ID berdasarkan kode yang sudah ada di repository ini.

Fokus hanya pada halaman input atau home page. Jangan mengubah struktur, tampilan, logika, ID elemen, maupun fitur pada halaman hasil kecuali benar-benar diperlukan agar navigasi tetap berfungsi.

Tujuan utama:
1. Membuat halaman input mudah dipahami pengguna awam.
2. Menghilangkan kesan template SaaS, AI-generated UI, atau vibe coding.
3. Mengurangi penggunaan card berlebihan.
4. Membuat alur pemeriksaan produk terasa sederhana, tenang, terpercaya, dan relevan dengan layanan kesehatan.
5. Mempertahankan seluruh fitur yang sudah ada.

Fitur input yang wajib tetap tersedia:
- Pemeriksaan menggunakan link produk.
- Pemeriksaan menggunakan foto barcode.
- Pemeriksaan menggunakan screenshot iklan.
- Pemeriksaan menggunakan teks klaim.
- Drag and drop file.
- Pilihan file dari perangkat.
- Status file yang sudah dipilih.
- Tombol pemeriksaan.
- Loading overlay.
- Navigasi ke bagian pemeriksaan.
- Penjelasan mengenai BPOM, analisis klaim, dan saran.
- Disclaimer bahwa hasil bukan pengganti tenaga kesehatan.

Perubahan struktur yang diminta:

1. Sederhanakan hero
- Gunakan satu judul utama yang jelas.
- Gunakan satu paragraf penjelasan singkat.
- Gunakan satu tombol utama menuju area pemeriksaan.
- Hilangkan side-note sebagai card terpisah.
- Informasi mengenai hasil pemeriksaan boleh dipindahkan menjadi teks kecil di bawah tombol utama.
- Jangan membuat hero terlalu tinggi.

2. Sederhanakan alur tiga langkah
- Pertahankan informasi alur pemeriksaan.
- Jangan tampilkan sebagai tiga card besar.
- Gunakan satu baris proses sederhana atau daftar langkah horizontal.
- Pada perangkat mobile, langkah boleh berubah menjadi susunan vertikal.
- Hindari shadow dan border pada setiap langkah.

3. Ubah empat pilihan metode input
- Jangan tampilkan empat metode sebagai card besar.
- Gunakan tab atau segmented navigation yang ringkas.
- Pilihan yang tersedia:
  Link Produk
  Barcode
  Screenshot
  Teks Klaim
- Hanya metode aktif yang memiliki penjelasan lengkap.
- Metode tidak aktif cukup menampilkan nama dan ikon sederhana bila memang diperlukan.
- Tetap tampilkan label “Direkomendasikan” untuk Link Produk, tetapi jangan menggunakan badge berlebihan.

4. Pertahankan satu panel input utama
- Gunakan satu container utama untuk seluruh metode.
- Isi panel berubah sesuai metode yang dipilih.
- Hindari card di dalam card.
- Hindari banyak border, shadow, badge, dan radius besar.
- Gunakan ruang kosong, tipografi, garis pemisah, dan hierarchy sebagai pembeda section.

5. Perbaiki panel Link Produk
- Tambahkan label input yang jelas, bukan hanya placeholder.
- Input dan tombol harus mudah ditemukan.
- Pada desktop, input dan tombol boleh sejajar.
- Pada mobile, tombol harus berada di bawah input dan memenuhi lebar container.
- Pertahankan helper text mengenai link halaman produk.

6. Perbaiki panel Barcode dan Screenshot
- Pertahankan drag and drop.
- Buat area upload terlihat jelas tetapi tidak seperti card dekoratif.
- Pertahankan tombol pilih file.
- Tampilkan nama file, ukuran file, atau status file setelah dipilih.
- Berikan opsi mengganti atau menghapus file.
- Jangan mengubah fungsi upload yang sudah ada.
- Gunakan bahasa yang mudah dimengerti.

7. Perbaiki panel Teks Klaim
- Gunakan label textarea yang jelas.
- Pertahankan contoh klaim pada placeholder.
- Tambahkan penghitung karakter bila mudah dilakukan tanpa mengganggu logika.
- Tombol pemeriksaan harus terlihat sebagai aksi utama.
- Jangan membuat textarea terlalu kecil.

8. Sederhanakan bagian “Yang Dicek”
- Pertahankan informasi:
  BPOM
  Klaim produk
  Saran sederhana
- Jangan tampilkan sebagai tiga card.
- Gunakan satu section dengan tiga kolom sederhana atau satu daftar horizontal.
- Gunakan garis pemisah bila diperlukan.
- Jangan menggunakan ikon dekoratif berlebihan.

9. Pertahankan disclaimer
- Jadikan disclaimer sebagai satu blok informasi sederhana.
- Jangan menggunakan card besar atau warna peringatan yang terlalu agresif.
- Pastikan teks tetap mudah dibaca.

Prinsip visual:
- Tidak menggunakan gradient.
- Tidak menggunakan glassmorphism.
- Tidak menggunakan efek glow.
- Tidak menggunakan shadow besar.
- Hindari radius yang terlalu bulat.
- Hindari terlalu banyak badge.
- Hindari penggunaan emoji.
- Jangan menjadikan setiap section sebagai card.
- Gunakan maksimal satu panel utama pada area input.
- Gunakan warna netral dengan satu warna aksen utama.
- Tampilan harus terasa profesional, tenang, dan kredibel.
- Prioritaskan keterbacaan daripada dekorasi.
- Jangan membuat tampilan seperti dashboard admin.
- Jangan membuat tampilan seperti landing page startup generik.

Tipografi dan hierarchy:
- Pastikan hanya terdapat satu H1.
- Gunakan H2 dan H3 sesuai struktur.
- Batasi panjang teks agar mudah dipindai.
- Gunakan ukuran teks minimal 16px untuk konten utama.
- Pastikan kontras warna memenuhi keterbacaan.
- Gunakan line-height yang nyaman.

Aksesibilitas:
- Tambahkan label yang terhubung dengan input menggunakan for dan id.
- Semua button harus memiliki type="button" bila tidak digunakan untuk submit form.
- Tambahkan aria-selected, aria-controls, dan role="tab" pada pilihan metode jika memakai pola tab.
- Pastikan seluruh metode dapat dipilih dengan keyboard.
- Tambahkan focus state yang jelas.
- Loading overlay harus menggunakan role="status" dan aria-live="polite".
- Jangan hanya mengandalkan warna untuk menunjukkan metode aktif.
- Pastikan area upload dapat digunakan dengan keyboard.

Responsiveness:
- Tampilan harus baik pada desktop, tablet, dan mobile.
- Jangan menggunakan fixed width yang menyebabkan overflow.
- Pada mobile, navigasi metode boleh horizontal-scroll atau tersusun dua kolom, tetapi harus tetap mudah digunakan.
- Input dan tombol utama harus memenuhi lebar layar pada mobile.
- Pastikan tidak ada teks atau tombol yang terpotong.

Struktur kode:
- Pertahankan pemisahan file HTML, CSS, dan JavaScript.
- Jangan menambahkan inline CSS.
- Jangan menambahkan inline JavaScript.
- Ganti class generik seperti u-style-* pada bagian input dengan nama class semantik.
- Contoh nama class:
  hero
  check-method-tabs
  check-method-tab
  check-panel
  upload-area
  input-helper
  trust-section
  disclaimer
- Jangan mengganti ID yang digunakan JavaScript kecuali seluruh referensinya diperbarui dengan aman.
- Jangan menambahkan framework atau dependency baru.
- Gunakan HTML, CSS, dan JavaScript yang sudah ada.
- Hapus CSS yang tidak lagi digunakan setelah revisi.
- Hindari duplikasi style.
- Buat kode mudah dibaca dan dipelihara.

Batas pekerjaan:
- Jangan menghapus fitur.
- Jangan mengubah endpoint API.
- Jangan mengubah payload request.
- Jangan mengubah cara backend menerima input.
- Jangan mengubah model analisis.
- Jangan mengubah halaman hasil.
- Jangan menambahkan fitur baru yang tidak diperlukan.
- Jangan membuat ulang project dari nol.
- Gunakan struktur repository saat ini.

Sebelum mengubah kode:
1. Periksa file HTML, CSS, dan JavaScript yang terkait.
2. Identifikasi ID dan selector yang digunakan JavaScript.
3. Pastikan perubahan HTML tidak merusak event listener.
4. Jelaskan secara singkat file yang akan diubah.

Setelah implementasi:
1. Pastikan keempat metode input masih dapat dipilih.
2. Pastikan panel aktif berubah dengan benar.
3. Pastikan upload barcode dan screenshot tetap bekerja.
4. Pastikan drag and drop tetap bekerja.
5. Pastikan tombol pemeriksaan masih menjalankan fungsi sebelumnya.
6. Pastikan loading overlay tetap bekerja.
7. Pastikan navigasi anchor tetap bekerja.
8. Pastikan tidak ada error JavaScript di console.
9. Uji tampilan pada lebar 375px, 768px, dan 1440px.
10. Jelaskan perubahan yang dilakukan dan file yang diubah.

Kerjakan revisi ini langsung pada kode yang ada. Jangan membuat mockup terpisah dan jangan mengubah halaman hasil.