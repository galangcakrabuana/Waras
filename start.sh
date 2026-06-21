#!/bin/bash

# Pastikan script dihentikan jika ada error
set -e

echo "=================================================="
echo "      MEMULAI APLIKASI WARAS-ID & SERVICE         "
echo "=================================================="

# 1. Jalankan Google Chrome dengan CDP Port 9222
echo "-> [1/3] Menjalankan Chrome dengan Remote Debugging (Port 9222)..."
/opt/google/chrome/chrome --remote-debugging-port=9222 --user-data-dir=/home/galang/.config/google-chrome-cdp --no-first-run --no-default-browser-check >/dev/null 2>&1 &
CHROME_CDP_PID=$!

sleep 2

# 2. Aktifkan venv dan jalankan Flask Backend
echo "-> [2/3] Menjalankan Flask Backend Server..."
source /home/galang/Documents/Website/venv/bin/activate
python /home/galang/Documents/Website/app.py &
FLASK_PID=$!p

sleep 4

# 3. Buka halaman aplikasi di Chrome
echo "-> [3/3] Membuka web aplikasi http://localhost:5000/..."
/opt/google/chrome/chrome http://localhost:5000/ >/dev/null 2>&1 &

echo "=================================================="
echo "   SEMUA SERVICE BERHASIL DIJALANKAN!             "
echo "   Tekan [Ctrl + C] untuk menutup semua service.  "
echo "=================================================="

# Bersihkan semua background process saat script di-close (Ctrl+C)
trap 'echo -e "\n-> Menghentikan semua service..."; kill $CHROME_CDP_PID $FLASK_PID 2>/dev/null || true; exit' INT TERM EXIT

# Tunggu proses backend
wait $FLASK_PID
