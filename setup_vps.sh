#!/bin/bash

# Konfigurasi VPS
VPS_USER="ubuntu"
VPS_IP="43.129.35.17"
VPS_HOST="${VPS_USER}@${VPS_IP}"
VPS_DIR="/home/ubuntu/waras-id"

echo "============================================================"
echo "          MEMULAI AUTOMATED SETUP FILE DI VPS               "
echo "============================================================"

# 1. Upload database waras_id.db dari lokal ke VPS
echo "-> [1/3] Mengunggah database waras_id.db ke VPS..."
scp ./waras_id.db ${VPS_HOST}:${VPS_DIR}/

if [ $? -eq 0 ]; then
    echo "✔ Database berhasil diunggah!"
else
    echo "❌ Gagal mengunggah database. Silakan periksa koneksi atau password."
    exit 1
fi

# 2. Jalankan perintah setup folder model & instalasi di VPS via SSH
echo "-> [2/3] Menghubungkan ke VPS untuk setup folder dan library..."
ssh -t ${VPS_HOST} "
    echo '-> Memeriksa folder model...';
    if [ -d '${VPS_DIR}/model' ]; then
        echo '-> Mengubah nama folder model ke indobert_overclaim_model...';
        mv ${VPS_DIR}/model ${VPS_DIR}/indobert_overclaim_model;
        echo '✔ Folder model berhasil diubah namanya!';
    elif [ -d '${VPS_DIR}/indobert_overclaim_model' ]; then
        echo '✔ Folder indobert_overclaim_model sudah ada.';
    else
        echo '⚠ Peringatan: Folder model tidak ditemukan di ${VPS_DIR}/model atau ${VPS_DIR}/indobert_overclaim_model.';
    fi

    echo '-> Membuat Virtual Environment...';
    cd ${VPS_DIR} && python3 -m venv venv;
    
    echo '-> Mengaktifkan venv & menginstal library...';
    source venv/bin/activate && \
    pip install --upgrade pip && \
    pip install flask flask-cors requests transformers torch easyocr playwright gunicorn && \
    playwright install chromium;

    echo '✔ Instalasi library selesai!';
"

if [ $? -eq 0 ]; then
    echo "============================================================"
    echo "✔ SEMUA FILE & LIBRARY DI VPS BERHASIL DI-SETUP!            "
    echo "============================================================"
else
    echo "❌ Terjadi kesalahan saat melakukan setup di VPS."
fi
