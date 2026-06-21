import os
import tempfile
import re
import requests
import json
import subprocess
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for communication with frontend

DB_PATH = os.getenv('DB_PATH', os.path.join(os.path.dirname(__file__), 'waras_id.db'))

@app.route('/')
def index():
    return send_file('preview (1).html')

# Lazy initialization of EasyOCR to speed up server start
ocr_reader = None

def get_ocr():
    global ocr_reader
    if ocr_reader is None:
        try:
            import easyocr
            print("Initializing EasyOCR...")
            ocr_reader = easyocr.Reader(['id', 'en'], gpu=False)
            print("EasyOCR initialized successfully.")
        except Exception as e:
            print(f"Error loading EasyOCR: {e}")
            ocr_reader = None
    return ocr_reader

# Lazy initialization of IndoBERT NLP model to speed up server start
nlp_model = None
nlp_tokenizer = None
labels = ["Normal Claim", "Overclaim"]

def get_nlp_classifier():
    global nlp_model, nlp_tokenizer, labels
    if nlp_model is None:
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            import torch
            print("Initializing IndoBERT NLP model...")
            model_path = os.path.join(os.path.dirname(__file__), "indobert_overclaim_model")
            nlp_tokenizer = AutoTokenizer.from_pretrained(model_path)
            nlp_model = AutoModelForSequenceClassification.from_pretrained(model_path)
            nlp_model.eval()
            
            # Load labels dynamically from model config
            if nlp_model.config.id2label:
                id2label = nlp_model.config.id2label
                sorted_keys = sorted(id2label.keys(), key=lambda x: int(x))
                labels = [id2label[k] for k in sorted_keys]
                
            print(f"IndoBERT NLP model initialized successfully with labels: {labels}")
        except Exception as e:
            print(f"Error loading NLP Model: {e}")
            nlp_model = None
            nlp_tokenizer = None
    return nlp_model, nlp_tokenizer

def predict_text(text):
    model, tokenizer = get_nlp_classifier()
    if model is None or tokenizer is None:
        return None
    try:
        import torch
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1).flatten().tolist()
            prediction = torch.argmax(logits, dim=1).item()
        
        return {
            "label": labels[prediction],
            "confidence": probabilities[prediction],
            "probabilities": dict(zip(labels, probabilities))
        }
    except Exception as e:
        print(f"Error predicting text with NLP: {e}")
        return None

def resolve_short_url(url):
    if 'shp.ee' in url or 'id.shp.ee' in url:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            # Gunakan requests.head untuk resolusi cepat. Jika gagal, gunakan requests.get.
            response = requests.head(url, headers=headers, allow_redirects=True, timeout=5)
            final_url = response.url
            print(f"Resolved short URL {url} to {final_url}")
            return final_url
        except Exception as e:
            print(f"Error resolving short URL with HEAD: {e}")
            try:
                response = requests.get(url, headers=headers, allow_redirects=True, timeout=5)
                final_url = response.url
                print(f"Resolved short URL with GET {url} to {final_url}")
                return final_url
            except Exception as ex:
                print(f"Error resolving short URL with GET: {ex}")
    return url

def extract_shopee_ids(url):
    # Pola 1: i.shopid.itemid
    match1 = re.search(r'i\.(\d+)\.(\d+)', url)
    if match1:
        return match1.group(1), match1.group(2)
        
    # Pola 2: product/shopid/itemid
    match2 = re.search(r'product/(\d+)/(\d+)', url)
    if match2:
        return match2.group(1), match2.group(2)
        
    return None, None

def fetch_shopee_product(shopid, itemid, full_url=None):
    # Phase 1: Direct API request (Fast fallback)
    api_url = f"https://shopee.co.id/api/v4/item/get?itemid={itemid}&shopid={shopid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://shopee.co.id/product/{shopid}/{itemid}",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    try:
        print(f"Fetching Shopee details via API for shopid: {shopid}, itemid: {itemid}...")
        response = requests.get(api_url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            item_data = data.get("data", {})
            if item_data:
                name = item_data.get("name", "")
                description = item_data.get("description", "")
                print("Shopee details fetched successfully via direct API.")
                return {"success": True, "description": f"{name}. {description}"}
        print(f"Direct API returned status code {response.status_code}. Falling back to Playwright CDP...")
    except Exception as e:
        print(f"Direct API error: {e}. Falling back to Playwright CDP...")

    # Phase 2: Playwright CDP browser automation (undoubtable cookie sharing)
    target_url = full_url or f"https://shopee.co.id/product/{shopid}/{itemid}"
    import sys
    try:
        python_exec = os.getenv('SHOPEE_PYTHON_EXEC', sys.executable)
        script_path = os.getenv('SHOPEE_FETCHER_SCRIPT', os.path.join(os.path.dirname(__file__), "shopee_stealth_fetcher.py"))
        print(f"Running stealth fetcher script via {python_exec} for URL: {target_url}...")
        res = subprocess.run([python_exec, script_path, target_url], capture_output=True, text=True, timeout=45)
        if res.returncode == 0:
            output_data = json.loads(res.stdout.strip())
            if output_data.get("success"):
                title = output_data.get("title", "")
                desc = output_data.get("description", "")
                full_text = f"{title}. {desc}"
                return {"success": True, "description": full_text}
            else:
                return {
                    "success": False,
                    "error_type": output_data.get("error_type"),
                    "error": output_data.get("error", "Gagal mengekstrak data dari halaman.")
                }
        else:
            print(f"Fetcher script stderr: {res.stderr}")
            return {"success": False, "error": f"Script error: {res.stderr}"}
    except Exception as ex:
        print(f"Error executing fetcher script: {ex}")
        return {"success": False, "error": f"Internal helper error: {ex}"}

import sqlite3
import adverse_event

def lookup_product(text):
    if not text:
        return None
        
    db_path = DB_PATH
    if not os.path.exists(db_path):
        print("Database waras_id.db not found. Skipping product lookup.")
        return None
        
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 1. Try search by BPOM registration number
        bpom_match = re.search(r'\b(?:POM\s+)?(TR|QD|QI|SD|SI|SL|NA|NB|NC|ND|NE|DKL|DKP|DKS|GKL|GKP|GKS)\s*(\d{9})\b', text, re.IGNORECASE)
        if bpom_match:
            prefix = bpom_match.group(1).upper()
            digits = bpom_match.group(2)
            print(f"Extracted BPOM code: {prefix}{digits}")
            cursor.execute("SELECT * FROM products WHERE registration_number LIKE ?", (f"%{digits}%",))
            row = cursor.fetchone()
            if row:
                print(f"Found product by BPOM: {row['product_name']}")
                conn.close()
                return dict(row)
                
        # 2. Try search by name (clean up name and search)
        cleaned_text = re.sub(r'[^\w\s]', ' ', text)
        words = [w for w in cleaned_text.split() if len(w) > 2]
        
        # Ignore common filler words and claim-related terms
        ignore_words = {
            "TABLET", "KAPSUL", "OBAT", "HERBAL", "STRIP", "BOTOL", "SIRUP", "CREAM", "KRIM", "GEL", "ORIGINAL", "ASLI", "PROMO", "MURAH", "READY", "STOCK",
            "DENGAN", "UNTUK", "PADA", "DARI", "OLEH", "ATAU", "DAN", "YANG", "BISA", "DAPAT", "AKAN", "TELAH", "SUDAH", "SECARA", "DALAM", "YAKNI", "SEPERTI",
            "MENYEMBUHKAN", "MENGOBATI", "MENCEGAH", "MEREDAKAN", "MENGATASI", "MENGHILANGKAN", "SEMBUH", "AMPUH", "MUJARAB", "MANJUR", "KHASIAT", "MANFAAT",
            "AMAN", "SEKETIKA", "INSTAN", "PERMANEN", "ABSOLUT", "TERBUKTI", "BEBAS", "ALAMI", "PALING", "SANGAT", "TERPERCAYA", "KHASIATNYA", "MANFAATNYA",
            "KANKER", "STROKE", "DIABETES", "KENCING", "MANIS", "TUMOR", "JANTUNG", "GINJAL", "KATARAK", "LUMPUH", "FLU", "BATUK", "DEMAM", "PANAS", "PUSING",
            "SAKIT", "GULA", "KOLESTEROL", "DARAH", "HIPERTENSI", "MAAG", "GERD", "ASAM", "URAT"
        }
        words = [w for w in words if w.upper() not in ignore_words]
        
        if words:
            # Try combinations
            search_term = " ".join(words[:3])
            cursor.execute("SELECT * FROM products WHERE product_name LIKE ? LIMIT 1", (f"%{search_term}%",))
            row = cursor.fetchone()
            if row:
                print(f"Found product by 3-word title: {row['product_name']}")
                conn.close()
                return dict(row)
                
            # Try searching by first word
            first_term = words[0]
            cursor.execute("SELECT * FROM products WHERE product_name LIKE ? LIMIT 1", (f"%{first_term}%",))
            row = cursor.fetchone()
            if row:
                print(f"Found product by first-word title: {row['product_name']}")
                conn.close()
                return dict(row)
        conn.close()
    except Exception as e:
        print(f"Error looking up product in DB: {e}")
    return None

def interpret_bpom_code(bpom_code):
    if not bpom_code:
        return "-"
    bpom_code = bpom_code.upper().strip()
    
    # Clean POM prefix out if present
    bpom_code = re.sub(r'^POM\s*', '', bpom_code)
    
    # Extract the prefix letters (non-digits at the beginning)
    match = re.match(r'^([A-Z]+)', bpom_code)
    if not match:
        return "Format Kode Tidak Dikenali"
        
    prefix = match.group(1)
    
    # Kategori Jamu, Herbal, Suplemen, Kosmetik (2 huruf)
    two_letter_map = {
        'TR': 'Obat Tradisional Lokal (Jamu Dalam Negeri)',
        'TI': 'Obat Tradisional Impor (Jamu dari Luar Negeri)',
        'HT': 'Obat Herbal Terstandar (OHT)',
        'FF': 'Fitofarmaka (Herbal Teruji Klinis)',
        'SD': 'Suplemen Kesehatan Dalam Negeri (Lokal)',
        'SI': 'Suplemen Kesehatan Impor (Luar Negeri)',
        'NA': 'Kosmetik Lokal / Asia',
        'NB': 'Kosmetik Impor',
        'NC': 'Kosmetik Impor',
        'ND': 'Kosmetik Impor',
        'NE': 'Kosmetik Impor',
    }
    
    if prefix in two_letter_map:
        return two_letter_map[prefix]
        
    # Kategori Obat Modern (3 huruf)
    if len(prefix) == 3:
        p1 = prefix[0]
        p2 = prefix[1]
        p3 = prefix[2]
        
        parts = []
        
        # Huruf Pertama (Jenis Penamaan)
        if p1 == 'D':
            parts.append("Obat Nama Dagang (Paten)")
        elif p1 == 'G':
            parts.append("Obat Generik")
        else:
            parts.append(f"Obat Kategori {p1}")
            
        # Huruf Kedua (Golongan Keamanan)
        if p2 == 'B':
            parts.append("Golongan Bebas (Bebas Dibeli)")
        elif p2 == 'T':
            parts.append("Golongan Bebas Terbatas")
        elif p2 == 'K':
            parts.append("Golongan Obat Keras (Wajib Resep Dokter)")
        elif p2 == 'P':
            parts.append("Golongan Psikotropika (Wajib Resep Dokter)")
        elif p2 == 'N':
            parts.append("Golongan Narkotika (Wajib Resep Dokter)")
        else:
            parts.append(f"Keamanan {p2}")
            
        # Huruf Ketiga (Asal)
        if p3 == 'L':
            parts.append("Buatan Lokal / Dalam Negeri")
        elif p3 == 'I':
            parts.append("Buatan Impor / Luar Negeri")
        else:
            parts.append(f"Asal {p3}")
            
        return " - ".join(parts)
        
    return f"Kode Reg. ({prefix})"

def get_atc_details(atc_code):
    if not atc_code:
        return None
    db_path = DB_PATH
    if not os.path.exists(db_path):
        return None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM atc_reference WHERE atc_code = ?", (atc_code.upper().strip(),))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
    except Exception as e:
        print(f"Error looking up ATC in DB: {e}")
    return None

def get_drug_function_layman(atc_code, category):
    atc_code = (atc_code or "").upper().strip()
    category = (category or "").lower()
    
    if atc_code.startswith("R05"):
        return {
            "layman_category": "Obat Batuk dan Flu",
            "indications": [
                "Membantu meredakan batuk",
                "Membantu meredakan pilek dan hidung tersumbat",
                "Membantu menurunkan demam ringan"
            ]
        }
    elif atc_code.startswith("N02B"):
        return {
            "layman_category": "Obat Pereda Nyeri dan Demam (Analgetik-Antipiretik)",
            "indications": [
                "Meringankan rasa sakit seperti sakit kepala",
                "Meringankan sakit gigi",
                "Membantu menurunkan demam"
            ]
        }
    elif atc_code.startswith("J01"):
        return {
            "layman_category": "Antibiotik",
            "indications": [
                "Mengobati infeksi bakteri",
                "Harus dihabiskan sesuai petunjuk resep dokter untuk mencegah resistensi bakteri"
            ]
        }
    elif atc_code.startswith("A02"):
        return {
            "layman_category": "Obat Lambung / Antasida",
            "indications": [
                "Meredakan asam lambung berlebih",
                "Mengatasi rasa perih/sakit maag",
                "Mengurangi perut kembung"
            ]
        }
    elif atc_code.startswith("B01"):
        return {
            "layman_category": "Antikoagulan / Pengencer Darah",
            "indications": [
                "Mencegah pembekuan darah",
                "Mengurangi risiko penyumbatan pembuluh darah"
            ]
        }
    elif atc_code.startswith("C09"):
        return {
            "layman_category": "Obat Darah Tinggi (Hipertensi)",
            "indications": [
                "Membantu menurunkan tekanan darah tinggi",
                "Menjaga dan memelihara kesehatan fungsi jantung"
            ]
        }
    elif "vitamin" in category or "suplemen" in category or "supplement" in category:
        return {
            "layman_category": "Suplemen Kesehatan / Vitamin",
            "indications": [
                "Membantu memenuhi kebutuhan vitamin/suplemen harian",
                "Menjaga dan memelihara daya tahan tubuh"
            ]
        }
    elif "jamu" in category or "tradisional" in category or "herbal" in category:
        return {
            "layman_category": "Obat Tradisional / Herbal",
            "indications": [
                "Memelihara kesehatan tubuh secara tradisional",
                "Membantu meredakan gejala penyakit ringan sesuai kearifan lokal"
            ]
        }
    
    return {
        "layman_category": "Kategori Terapi Umum",
        "indications": [
            "Digunakan sesuai petunjuk dokter atau indikasi umum pada kemasan produk"
        ]
    }

def extract_trigger_words(text):
    trigger_words = [
        'sembuh total', 'tanpa efek samping', 'ampuh', 'permanen', 
        '100% aman', '100% ampuh', 'mujarab', 'paling ampuh', 
        'seketika', 'instan', 'menyembuhkan segala', 'terbukti menyembuhkan'
    ]
    found = []
    text_lower = text.lower()
    for word in trigger_words:
        if word in text_lower:
            found.append(word)
    return found

def get_route_layman(route):
    if not route:
        return "Sesuai indikasi kemasan"
    route_upper = route.upper().strip()
    route_lower = route.lower()
    
    # Check exact abbreviation first
    if route_upper == 'O':
        return "Diminum (Oral)"
    elif route_upper == 'P':
        return "Suntik / Infus (Parenteral)"
    elif route_upper == 'R':
        return "Melalui anus (Rektal)"
    elif route_upper == 'N':
        return "Tetes/semprot hidung (Nasal)"
    elif route_upper in ['TD', 'SL']:
        return "Oles / Tempel Kulit (Transdermal)"
    elif route_upper in ['IH', 'INHAL']:
        return "Hirup (Inhalasi)"
    elif route_upper == 'V':
        return "Melalui vagina (Vaginal)"
        
    # Fallback to substring matching
    if 'oral' in route_lower:
        return "Diminum (Oral)"
    elif 'parenteral' in route_lower or 'injection' in route_lower or 'intravenous' in route_lower or 'intramuscular' in route_lower:
        return "Suntik / Infus (Parenteral)"
    elif 'inhal' in route_lower:
        return "Hirup (Inhalasi)"
    elif 'rectal' in route_lower:
        return "Melalui anus (Rektal)"
    elif 'nasal' in route_lower:
        return "Tetes/semprot hidung (Nasal)"
    elif 'cutaneous' in route_lower or 'transdermal' in route_lower or 'topical' in route_lower:
        return "Oles / Tempel Kulit (Transdermal)"
    return route

def save_analysis_to_db(product_id, analyzed_text, label, confidence, trigger_words, consistency_score, claim_score, safety_score, recommendation):
    db_path = DB_PATH
    if not os.path.exists(db_path):
        return
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Map label string to int
        label_map = {
            "tidak overclaim": 0,
            "overclaim sedang": 1,
            "overclaim tinggi": 2,
            "normal claim": 0,
            "overclaim": 2
        }
        pred_label_int = label_map.get(label.lower() if label else "", 0)
        
        # Insert to claim_analysis
        cursor.execute("""
            INSERT INTO claim_analysis (product_id, analyzed_text, prediction_label, confidence_score, detected_claims)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, analyzed_text, pred_label_int, confidence, json.dumps(trigger_words)))
        
        # Insert to product_analysis
        cursor.execute("""
            INSERT INTO product_analysis (product_id, claim_score, consistency_score, safety_score, recommendation)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, claim_score, consistency_score, safety_score, recommendation))
        
        conn.commit()
        conn.close()
        print("Analysis successfully saved to database.")
    except Exception as e:
        print(f"Error saving analysis to DB: {e}")

def get_therapeutic_group(atc_code, category):
    atc_code = (atc_code or "").upper().strip()
    category = (category or "").strip()
    
    if atc_code.startswith("C09A"):
        return "ACE Inhibitor"
    elif atc_code.startswith("C09C"):
        return "Angiotensin II Antagonists"
    elif atc_code.startswith("R05"):
        return "Ekspektoran / Mukolitik / Obat Batuk"
    elif atc_code.startswith("N02B"):
        return "Analgetik / Antipiretik"
    elif atc_code.startswith("J01"):
        return "Antibakteri / Antibiotik"
    elif atc_code.startswith("A02"):
        return "Antasida / Anti-Ulkus"
    elif atc_code.startswith("B01"):
        return "Antikoagulan"
    elif atc_code:
        return f"Golongan Obat ({atc_code[:3]})"
    return category or "Tidak Tergolongkan"

def get_administration_route_standard(route):
    if not route:
        return "-"
    route_upper = route.upper().strip()
    if route_upper == 'O':
        return "Oral"
    elif route_upper == 'P':
        return "Parenteral"
    elif route_upper == 'R':
        return "Rectal"
    elif route_upper == 'N':
        return "Nasal"
    elif route_upper in ['TD', 'SL']:
        return "Transdermal"
    elif route_upper in ['IH', 'INHAL']:
        return "Inhalation"
    elif route_upper == 'V':
        return "Vaginal"
    return route

def get_media_penggunaan(route):
    if not route:
        return "Sesuai indikasi kemasan"
    route_upper = route.upper().strip()
    if route_upper == 'O':
        return "Diminum"
    elif route_upper == 'P':
        return "Disuntikkan / Diinfuskan"
    elif route_upper == 'R':
        return "Dimasukkan melalui anus"
    elif route_upper == 'N':
        return "Diteteskan / Disemprotkan ke hidung"
    elif route_upper in ['TD', 'SL']:
        return "Dioleskan / Ditempelkan pada kulit"
    elif route_upper in ['IH', 'INHAL']:
        return "Dihirup"
    elif route_upper == 'V':
        return "Dimasukkan melalui vagina"
    return "Sesuai petunjuk kemasan"

def extract_trigger_sentences(text, trigger_words):
    if not text or not trigger_words:
        return []
    sentences = re.split(r'[.!?\n]+', text)
    found_sentences = []
    for s in sentences:
        s_clean = s.strip()
        if not s_clean:
            continue
        s_lower = s_clean.lower()
        for word in trigger_words:
            if word in s_lower:
                if s_clean not in found_sentences:
                    found_sentences.append(s_clean)
                break
    return found_sentences

def generate_ai_summary(product, claim_analysis, medical_consistency, final_verdict):
    if final_verdict == "Data Tidak Lengkap":
        return "Sistem tidak dapat melakukan analisis secara komprehensif karena informasi produk tidak ditemukan dalam database BPOM dan tidak ada deskripsi klaim yang cukup untuk diperiksa."
        
    product_name = product.get("product_name") if product else "Produk"
    category = product.get("product_category", "produk kesehatan") if product else "produk"
    
    part1 = f"Produk {product_name} merupakan {category.lower()} yang terdaftar resmi di BPOM." if product else "Produk tidak terdaftar pada database resmi BPOM."
    
    nlp_label = claim_analysis.get("label", "").lower()
    trigger_words = claim_analysis.get("trigger_words", [])
    
    if nlp_label in ["overclaim tinggi", "overclaim"]:
        part2 = "Teks yang dianalisis terindikasi mengandung klaim berlebihan (Overclaim Tinggi)."
        if trigger_words:
            part2 += f" Ditemukan beberapa frasa promosi absolut atau berlebih seperti: {', '.join(trigger_words)}."
    elif nlp_label == "overclaim sedang":
        part2 = "Teks yang dianalisis terindikasi mengandung klaim cukup berlebihan (Overclaim Sedang)."
        if trigger_words:
            part2 += f" Ditemukan beberapa kata pemicu iklan seperti: {', '.join(trigger_words)}."
    else:
        part2 = "Teks deskripsi produk tidak mengandung klaim kesehatan yang berlebihan (tidak overclaim)."
        
    score = medical_consistency.get("score", 100)
    
    if score < 50:
        part3 = f"Hasil analisis konsistensi medis menunjukkan ketidaksesuaian kritis ({score}/100) karena ditemukan klaim penyembuhan penyakit berat yang tidak relevan dengan kategori terapi."
    elif score < 90:
        part3 = f"Hasil analisis konsistensi medis menunjukkan nilai sedang ({score}/100) karena klaim promosi melebihi indikasi terdaftar."
    else:
        part3 = f"Klaim promosi sejalan dan konsisten dengan fungsi terapi terdaftar ({score}/100)."
        
    part4 = f"Berdasarkan hasil analisis terintegrasi, sistem menyimpulkan status akhir produk sebagai {final_verdict.upper()}."
    
    return f"{part1} {part2} {part3} {part4}"

def calculate_consistency_score(product, prediction_result, extracted_text):
    serious_disease_triggers = {
        'diabetes': 'diabetes', 'kencing manis': 'diabetes', 
        'kanker': 'kanker', 'cancer': 'kanker', 
        'tumor': 'tumor', 'stroke': 'stroke', 
        'ginjal': 'gagal ginjal', 'katarak': 'katarak', 
        'jantung': 'jantung'
    }
    
    text_lower = extracted_text.lower() if extracted_text else ""
    detected_diseases = []
    for trig, canonical in serious_disease_triggers.items():
        if trig in text_lower:
            if canonical not in detected_diseases:
                detected_diseases.append(canonical)
                
    pred_label = prediction_result.get("label", "").lower() if prediction_result else "tidak overclaim"
    trigger_words = extract_trigger_words(extracted_text)
    
    reasons = []
    
    if not product:
        reasons.append({"icon": "cross", "text": "Produk tidak terdaftar di BPOM"})
        if detected_diseases:
            for d in detected_diseases:
                reasons.append({"icon": "cross", "text": f"Klaim menyembuhkan {d}"})
        if pred_label in ["overclaim tinggi", "overclaim"]:
            reasons.append({"icon": "cross", "text": "Klaim iklan terindikasi berlebihan"})
            return 50, "Produk tidak terdaftar di BPOM. Klaim iklan terindikasi berlebihan (Overclaim).", reasons
        else:
            reasons.append({"icon": "check", "text": "Tidak terindikasi klaim ekstrim"})
            return 70, "Produk tidak terdaftar di BPOM. Konsistensi klaim medis tidak dapat dinilai sepenuhnya.", reasons
            
    cat = (product.get("product_category") or "").lower()
    is_supplement_or_herbal = any(x in cat for x in ["vitamin", "suplemen", "supplement", "mineral", "traditional", "jamu", "herbal", "kosmetik", "cosmetic"])
    
    reasons.append({"icon": "check", "text": "Produk terdaftar resmi di BPOM"})
    
    if is_supplement_or_herbal:
        if detected_diseases:
            for d in detected_diseases:
                reasons.append({"icon": "cross", "text": f"Klaim menyembuhkan {d}"})
            reasons.append({"icon": "cross", "text": "Tidak sesuai fungsi produk suplemen"})
            if trigger_words:
                reasons.append({"icon": "cross", "text": "Mengandung klaim absolut"})
            return 15, "Tidak sesuai kategori terapi (Produk suplemen/tradisional diklaim mengobati penyakit kronis); Mengandung klaim pengobatan penyakit berat/kronis secara mandiri; Tidak didukung fungsi produk yang terdaftar di BPOM.", reasons
        elif pred_label == "overclaim tinggi":
            reasons.append({"icon": "cross", "text": "Mengandung klaim berlebihan untuk suplemen"})
            if trigger_words:
                reasons.append({"icon": "cross", "text": "Mengandung klaim absolut"})
            return 35, "Mengandung klaim berlebihan (Overclaim Tinggi) untuk kategori produk suplemen/herbal.", reasons
        elif pred_label == "overclaim sedang":
            reasons.append({"icon": "cross", "text": "Mengandung klaim sedang untuk suplemen"})
            return 60, "Klaim iklan terindikasi cukup berlebihan (Overclaim Sedang) untuk kategori suplemen/herbal.", reasons
        else:
            reasons.append({"icon": "check", "text": "Klaim sesuai kategori terapi"})
            reasons.append({"icon": "check", "text": "Tidak ditemukan klaim di luar indikasi"})
            reasons.append({"icon": "check", "text": "Tidak ditemukan kata absolut"})
            return 95, "Sesuai. Klaim konsisten dengan kategori suplemen/obat tradisional tanpa klaim pengobatan berlebih.", reasons
    else:
        # Standard medicine / drug
        if detected_diseases and pred_label == "overclaim tinggi":
            for d in detected_diseases:
                reasons.append({"icon": "cross", "text": f"Klaim menyembuhkan {d}"})
            reasons.append({"icon": "cross", "text": "Tidak sesuai fungsi obat"})
            if trigger_words:
                reasons.append({"icon": "cross", "text": "Mengandung klaim absolut"})
            return 30, "Peringatan! Deskripsi atau iklan menggunakan klaim berlebih (Overclaim Tinggi) yang tidak diizinkan untuk promosi obat.", reasons
        elif pred_label == "overclaim sedang":
            reasons.append({"icon": "cross", "text": "Klaim iklan melebihi indikasi resmi"})
            return 65, "Peringatan! Deskripsi menggunakan klaim cukup berlebih (Overclaim Sedang) untuk obat terdaftar.", reasons
        else:
            reasons.append({"icon": "check", "text": "Klaim sesuai kategori terapi"})
            reasons.append({"icon": "check", "text": "Tidak ditemukan klaim di luar indikasi"})
            reasons.append({"icon": "check", "text": "Tidak ditemukan kata absolut"})
            return 100, "Klaim konsisten dengan indikasi dan kategori terapi resmi yang terdaftar di BPOM.", reasons

def calculate_safety_score(product_found, prediction_result, adverse_events, consistency_score, extracted_text):
    # 1. BPOM Verification (Weight: 25%)
    bpom_score = 100 if product_found else 0
    
    # 2. Medical Consistency (Weight: 35%)
    # consistency_score is passed directly
    
    # 3. NLP Claim Analysis (Weight: 25%)
    pred_label = prediction_result.get("label", "").lower() if prediction_result else "tidak overclaim"
    if pred_label in ["overclaim tinggi", "overclaim"]:
        claim_score = 0
    elif pred_label == "overclaim sedang":
        claim_score = 50
    else:
        claim_score = 100
        
    # 4. OpenFDA Safety Insight (Weight: 15%)
    ae_score = 100
    total_reports = adverse_events.get("total_reports", 0)
    serious_reports = adverse_events.get("seriousness", {}).get("serious", 0)
    
    if total_reports > 0:
        serious_ratio = serious_reports / total_reports
        ae_score = max(0, 100 - min(70, int(serious_ratio * 100) + min(20, int(total_reports / 5000))))
        
    final_score = int(
        (bpom_score * 0.25) +
        (consistency_score * 0.35) +
        (claim_score * 0.25) +
        (ae_score * 0.15)
    )
    
    trigger_words = extract_trigger_words(extracted_text)
    
    # Verdict Categorization (Aman, Cukup Aman, Perlu Perhatian, Potensi Overclaim, Risiko Tinggi, Data Tidak Lengkap)
    if not product_found and (not extracted_text or len(extracted_text.strip()) < 5):
        recommendation = "Data Tidak Lengkap"
    else:
        if final_score >= 81:
            recommendation = "Aman"
        elif final_score >= 61:
            recommendation = "Cukup Aman"
        elif final_score >= 31:
            if pred_label in ["overclaim tinggi", "overclaim"]:
                recommendation = "Potensi Overclaim"
            else:
                recommendation = "Perlu Perhatian"
        else:
            recommendation = "Risiko Tinggi"
            
    # Alasan Skor lists
    reasons_list = []
    if product_found:
        reasons_list.append({"icon": "check", "text": "Produk terdaftar BPOM"})
    else:
        reasons_list.append({"icon": "cross", "text": "Produk tidak terdaftar BPOM"})
        
    if pred_label in ["overclaim tinggi", "overclaim", "overclaim sedang"]:
        reasons_list.append({"icon": "cross", "text": "Klaim overclaim terdeteksi"})
    else:
        reasons_list.append({"icon": "check", "text": "Bebas overclaim"})
        
    if consistency_score >= 80:
        reasons_list.append({"icon": "check", "text": "Klaim sesuai indikasi"})
    else:
        reasons_list.append({"icon": "cross", "text": "Klaim tidak sesuai indikasi"})
        
    if len(trigger_words) > 0:
        reasons_list.append({"icon": "cross", "text": "Mengandung klaim absolut"})
    else:
        reasons_list.append({"icon": "check", "text": "Bebas klaim absolut"})
        
    return {
        "final_score": final_score,
        "bpom_score": bpom_score,
        "claim_score": claim_score,
        "consistency_score": consistency_score,
        "adverse_event_score": ae_score,
        "recommendation": recommendation,
        "reasons": reasons_list
    }

@app.route('/api/check', methods=['POST'])
def process_ocr():
    req_type = request.form.get('type')
    
    # Handle JSON payload as well
    if request.is_json:
        data = request.get_json()
        req_type = data.get('type')
        text = data.get('text', '')
        url = data.get('url', '')
    else:
        text = request.form.get('text', '')
        url = request.form.get('url', '')

    print(f"Received request. Type: {req_type}")

    extracted_text = ""

    if req_type == 'text':
        extracted_text = text
    elif req_type == 'link':
        resolved_url = resolve_short_url(url)
        if 'shopee.co.id' in resolved_url:
            shopid, itemid = extract_shopee_ids(resolved_url)
            if shopid and itemid:
                res_data = fetch_shopee_product(shopid, itemid, full_url=resolved_url)
                if res_data.get("success"):
                    extracted_text = res_data.get("description", "")
                else:
                    err_msg = res_data.get("error", "Gagal mengambil data produk dari Shopee.")
                    if res_data.get("error_type") == "cdp_closed":
                        return jsonify({
                            "status": "error",
                            "message": "Chrome Debugging Port (9222) tidak aktif. Pastikan Chrome telah dijalankan dengan command: /opt/google/chrome/chrome --remote-debugging-port=9222"
                        }), 400
                    else:
                        return jsonify({
                            "status": "error",
                            "message": err_msg
                        }), 400
            else:
                return jsonify({
                    "status": "error",
                    "message": "Link Shopee tidak valid atau ID produk/toko tidak ditemukan."
                }), 400
        else:
            extracted_text = url
    elif req_type in ['screenshot', 'barcode']:
        file = request.files.get('image')
        if not file:
            return jsonify({
                "status": "error",
                "message": "File gambar tidak ditemukan dalam request."
            }), 400
        
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)
        print(f"Saved temp image to {temp_path}")

        try:
            ocr = get_ocr()
            if ocr is None:
                return jsonify({
                    "status": "error",
                    "message": "OCR engine gagal diinisialisasi."
                }), 500

            print("Running OCR on image...")
            result = ocr.readtext(temp_path)
            lines = [entry[1] for entry in result if entry[1].strip()]
            extracted_text = " ".join(lines)
            print(f"OCR Extracted Text: {extracted_text}")
        except Exception as e:
            print(f"Error executing OCR: {e}")
            return jsonify({
                "status": "error",
                "message": f"Gagal menjalankan OCR: {str(e)}"
            }), 500
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
                print(f"Removed temp image {temp_path}")
    else:
        return jsonify({
            "status": "error",
            "message": "Metode input tidak valid."
        }), 400

    # 1. NLP Overclaim Prediction
    prediction_result = None
    if extracted_text.strip():
        prediction_result = predict_text(extracted_text)

    # 2. Database Lookup
    search_context = extracted_text if extracted_text.strip() else (text or url)
    product_found = lookup_product(search_context)
    
    product_profile = None
    atc_ref = None
    adverse_events = {
        "ingredients": [],
        "total_reports": 0,
        "side_effects": [],
        "seriousness": {"serious": 0, "non_serious": 0}
    }
    
    if product_found:
        atc_ref = get_atc_details(product_found.get("atc_code"))
        product_profile = {
            "id": product_found.get("id"),
            "product_name": product_found.get("product_name"),
            "registration_number": product_found.get("registration_number"),
            "manufacturer": product_found.get("manufacturer"),
            "product_category": product_found.get("product_category"),
            "ingredient": product_found.get("ingredient"),
            "atc_code": product_found.get("atc_code")
        }
        # 3. Query OpenFDA / Cache for Adverse Events
        if product_found.get("ingredient"):
            adverse_events = adverse_event.get_product_adverse_events(product_found.get("ingredient"))
    else:
        # Fallback to direct extraction if not in DB
        direct_ingredients = adverse_event.extract_ingredients(search_context)
        if direct_ingredients:
            adverse_events = adverse_event.get_product_adverse_events(", ".join(direct_ingredients))
            product_profile = {
                "id": None,
                "product_name": "Tidak Terdaftar (Hasil OCR/Iklan)",
                "registration_number": "Belum Terverifikasi BPOM",
                "manufacturer": "Tidak Diketahui",
                "product_category": "Tidak Teridentifikasi",
                "ingredient": ", ".join(direct_ingredients),
                "atc_code": None
            }

    # 4. Consistency Scoring
    consistency_score, consistency_explanation, consistency_reasons = calculate_consistency_score(product_found, prediction_result, extracted_text)
    consistency = {
        "score": consistency_score,
        "explanation": consistency_explanation,
        "reasons": consistency_reasons
    }

    # 5. Final Safety Score and Recommendation
    safety_score = calculate_safety_score(product_found, prediction_result, adverse_events, consistency_score, extracted_text)

    # 6. Drug Function layman layer
    atc_code = product_found.get("atc_code") if product_found else None
    cat = product_found.get("product_category") if product_found else None
    drug_function = get_drug_function_layman(atc_code, cat)

    # 7. DDD dosage layer
    ddd_dosage = {
        "ddd": atc_ref.get("ddd") if atc_ref else None,
        "uom": atc_ref.get("uom") if atc_ref else None,
        "administration_route": get_administration_route_standard(atc_ref.get("administration_route")) if atc_ref else "-",
        "administration_route_layman": get_route_layman(atc_ref.get("administration_route")) if atc_ref else "Sesuai indikasi kemasan",
        "media_penggunaan": get_media_penggunaan(atc_ref.get("administration_route")) if atc_ref else "Sesuai petunjuk kemasan",
        "disclaimer": "DDD merupakan standar dosis referensi WHO untuk tujuan klasifikasi dan analisis obat. DDD bukan petunjuk penggunaan langsung bagi pasien."
    }

    # 8. Explainable AI Trigger words
    trigger_words = extract_trigger_words(extracted_text)
    trigger_sentences = extract_trigger_sentences(extracted_text, trigger_words)
    claim_analysis = {
        "label": prediction_result.get("label") if prediction_result else "tidak overclaim",
        "confidence": prediction_result.get("confidence") if prediction_result else 1.0,
        "trigger_words": trigger_words,
        "trigger_sentences": trigger_sentences
    }

    # 9. OpenFDA Safety Insight details with disclaimer
    openfda_safety_insight = {
        "ingredient_queried": product_found.get("ingredient") if product_found else (direct_ingredients[0] if direct_ingredients else "-"),
        "total_reports": adverse_events.get("total_reports", 0),
        "serious_reports": adverse_events.get("seriousness", {}).get("serious", 0),
        "side_effects": adverse_events.get("side_effects", []),
        "disclaimer": "Data OpenFDA berasal dari laporan adverse event global berdasarkan zat aktif. Data ini tidak menunjukkan bahwa produk tertentu pasti menyebabkan efek samping tersebut. Informasi digunakan sebagai referensi keamanan tambahan."
    }

    # 10. AI Executive Summary
    ai_exec_summary = generate_ai_summary(product_found, claim_analysis, consistency, safety_score.get("recommendation"))

    # Extract raw BPOM code if matched
    raw_bpom = None
    if product_found and product_found.get("registration_number"):
        raw_bpom = product_found.get("registration_number")
    else:
        # Try to find a BPOM pattern in the context
        ctx = extracted_text if extracted_text.strip() else (text or url or "")
        m = re.search(r'\b(?:POM\s+)?(TR|QD|QI|SD|SI|SL|NA|NB|NC|ND|NE|DKL|DKP|DKS|GKL|GKP|GKS)\s*(\d{9})\b', ctx, re.IGNORECASE)
        if m:
            raw_bpom = f"{m.group(1).upper()} {m.group(2)}"

    # Refine product profile to include "therapeutic_group" and "atc_code"
    product_profile_refined = {
        "id": product_found.get("id") if product_found else None,
        "product_name": product_found.get("product_name") if product_found else ("Tidak Terdaftar" if extracted_text else "-"),
        "registration_number": product_found.get("registration_number") if product_found else (raw_bpom if raw_bpom else ("Belum Terverifikasi BPOM" if extracted_text else "-")),
        "manufacturer": product_found.get("manufacturer") if product_found else ("Tidak Diketahui" if extracted_text else "-"),
        "product_category": product_found.get("product_category") if product_found else ("Tidak Teridentifikasi" if extracted_text else "-"),
        "ingredient": product_found.get("ingredient") if product_found else (", ".join(direct_ingredients) if direct_ingredients else "-"),
        "therapeutic_group": get_therapeutic_group(product_found.get("atc_code") if product_found else None, product_found.get("product_category") if product_found else ""),
        "atc_code": product_found.get("atc_code") if product_found else "-",
        "bpom_interpretation": interpret_bpom_code(raw_bpom)
    }

    # 11. Verdict Details (for Section 1: Final Verdict)
    verdict_details = {
        "product_name": product_profile_refined.get("product_name"),
        "active_ingredient": product_profile_refined.get("ingredient"),
        "score": safety_score.get("final_score"),
        "direct_explanation": consistency_explanation
    }

    # 12. Save analysis to Database (SQLite)
    pred_label = prediction_result.get("label") if prediction_result else "tidak overclaim"
    pred_conf = prediction_result.get("confidence") if prediction_result else 1.0
    save_analysis_to_db(
        product_id=product_found.get("id") if product_found else None,
        analyzed_text=extracted_text,
        label=pred_label,
        confidence=pred_conf,
        trigger_words=trigger_words,
        consistency_score=consistency_score,
        claim_score=safety_score.get("claim_score"),
        safety_score=safety_score.get("final_score"),
        recommendation=safety_score.get("recommendation")
    )

    # Return structure matching exactly section 10 ("Final Output Structure")
    return jsonify({
        "status": "success",
        "final_verdict": safety_score.get("recommendation"),
        "verdict_details": verdict_details,
        "ai_executive_summary": ai_exec_summary,
        "consumer_safety_score": safety_score,
        "product_profile": product_profile_refined,
        "drug_function": drug_function,
        "ddd_dosage": ddd_dosage,
        "claim_analysis": claim_analysis,
        "medical_consistency": consistency,
        "openfda_safety_insight": openfda_safety_insight,
        "extracted_text": extracted_text,
        "recommendation": safety_score.get("recommendation"),
        "disclaimer": "WARAS-ID adalah platform analisis keselamatan konsumen bertenaga AI. Seluruh analisis bersifat informatif dan tidak menggantikan nasihat medis profesional dari dokter atau apoteker berlisensi."
    })

def identity_search_by_text(query):
    """Search product identity by name or BPOM number."""
    if not query or not query.strip():
        return {"status": "not_found"}

    product = lookup_product(query)
    if not product:
        return {"status": "not_found"}

    # Determine match quality
    query_upper = query.strip().upper()
    reg_num = (product.get("registration_number") or "").upper()
    name = (product.get("product_name") or "").upper()

    match_type = "full"
    # If user searched by reg number, check if name also partially matches
    bpom_match = re.search(r'\b(?:POM\s+)?(TR|QD|QI|SD|SI|SL|NA|NB|NC|ND|NE|DKL|DKP|DKS|GKL|GKP|GKS)\s*(\d{9})\b', query, re.IGNORECASE)
    if bpom_match:
        # Searched by reg number — always "full" if found
        match_type = "full"
    else:
        # Searched by name — check how close the match is
        query_words = set(query_upper.split())
        name_words = set(name.split())
        overlap = query_words & name_words
        if len(overlap) < len(query_words) * 0.5:
            match_type = "partial"

    return {
        "status": "found" if match_type == "full" else "partial",
        "match": match_type,
        "product": {
            "product_name": product.get("product_name"),
            "registration_number": product.get("registration_number"),
            "product_category": product.get("product_category"),
            "manufacturer": product.get("manufacturer"),
            "ingredient": product.get("ingredient"),
            "atc_code": product.get("atc_code")
        }
    }


@app.route('/api/products/identity-check', methods=['POST'])
def identity_check_text():
    data = request.get_json(silent=True)
    if not data or not data.get('query'):
        return jsonify({"status": "not_found", "message": "Masukkan nama atau nomor BPOM terlebih dahulu."}), 400

    query = data['query'].strip()
    print(f"Identity check (text): {query}")
    result = identity_search_by_text(query)
    return jsonify(result)


@app.route('/api/products/identity-check/barcode', methods=['POST'])
def identity_check_barcode():
    file = request.files.get('image')
    if not file:
        return jsonify({"status": "not_found", "message": "File gambar tidak ditemukan."}), 400

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)
    file.save(temp_path)

    try:
        ocr = get_ocr()
        if ocr is None:
            return jsonify({"status": "error", "message": "OCR engine gagal diinisialisasi."}), 500

        ocr_result = ocr.readtext(temp_path)
        lines = [entry[1] for entry in ocr_result if entry[1].strip()]
        extracted_text = " ".join(lines)
        print(f"Identity barcode OCR: {extracted_text}")

        if not extracted_text.strip():
            return jsonify({"status": "not_found", "message": "Barcode belum berhasil dibaca."})

        result = identity_search_by_text(extracted_text)
        return jsonify(result)
    except Exception as e:
        print(f"Identity barcode OCR error: {e}")
        return jsonify({"status": "error", "message": f"Gagal membaca barcode: {str(e)}"}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == '__main__':
    # Run server locally on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

