import re
import json
import sqlite3
import requests
from datetime import datetime, timedelta
import os

DB_PATH = os.getenv('DB_PATH', os.path.join(os.path.dirname(__file__), 'waras_id.db'))

def extract_ingredients(ingredient_text):
    """
    Cleans and extracts individual active ingredients from BPOM ingredients string.
    Example input: "Tiap tablet mengandung: Paracetamol 500 mg, Kafein 50 mg"
    Example output: ["PARACETAMOL", "KAFEIN"]
    """
    if not ingredient_text:
        return []
    
    # Convert to lowercase
    text = ingredient_text.lower()
    
    # Remove common prefix like "tiap tablet mengandung:", "tiap ml mengandung:", etc.
    text = re.sub(r'tiap\s+\w+\s+(mengandung|berisi)\s*:\s*', '', text)
    text = re.sub(r'mengandung\s*:\s*', '', text)
    
    # Split by comma, semicolon, newline, or plus sign
    raw_ingredients = re.split(r'[,;\n\+]', text)
    
    clean_ingredients = []
    for ing in raw_ingredients:
        ing = ing.strip()
        if not ing:
            continue
            
        # Split by "setara dengan", "equivalent to", "eq." to get the core ingredient
        ing = re.split(r'\b(setara dengan|equivalent to|eq\.?|as)\b', ing)[0].strip()
        
        # Remove numbers and units like "500 mg", "400mg", "10 mcg", "2g", "5 ml", etc.
        ing = re.sub(r'\b\d+[\s\.]*(mg|mcg|g|ml|iu|%)\b', '', ing)
        ing = re.sub(r'\b\d+\b', '', ing) # remove standalone numbers
        
        # Remove salt forms and chemical prefixes/suffixes
        suffixes = [
            'hcl', 'sulfate', 'sulfat', 'phosphate', 'fosfat', 'maleate', 'maleat',
            'sodium', 'natrium', 'potassium', 'kalium', 'calcium', 'kalsium',
            'monohydrate', 'dihydrate', 'trihydrate', 'hemihydrate', 'hydrate',
            'anhidrat', 'anhydrous', 'mesylate', 'fumarate', 'fumarat', 'hydrochloride',
            'acetate', 'citrate', 'carbonate', 'chloride'
        ]
        pattern = r'\b(' + '|'.join(suffixes) + r')\b'
        ing = re.sub(pattern, '', ing)
        
        # Clean up double spaces, punctuation
        ing = re.sub(r'[^\w\s-]', ' ', ing) # remove non-alphanumeric except spaces and hyphens
        ing = ' '.join(ing.split())
        
        # We only keep ingredients that have reasonable lengths
        if ing and len(ing) > 2:
            clean_ingredients.append(ing.upper())
            
    return clean_ingredients

def fetch_openfda_data(ingredient):
    """
    Queries OpenFDA API for adverse events of a specific active ingredient.
    """
    url_base = "https://api.fda.gov/drug/event.json"
    
    try:
        # 1. Get total reports and seriousness count
        url_serious = f"{url_base}?search=patient.drug.activesubstance.activesubstancename:\"{ingredient}\"&count=serious"
        res_serious = requests.get(url_serious, timeout=10)
        
        total_reports = 0
        serious_count = 0
        non_serious_count = 0
        
        if res_serious.status_code == 200:
            data = res_serious.json()
            results = data.get("results", [])
            for r in results:
                term = r.get("term") # 1 = serious, 2 = non-serious
                count = r.get("count", 0)
                if term == 1:
                    serious_count = count
                elif term == 2:
                    non_serious_count = count
            total_reports = serious_count + non_serious_count
        elif res_serious.status_code == 404:
            # Ingredient not found in OpenFDA records
            return {
                "success": True,
                "total_reports": 0,
                "side_effects": [],
                "seriousness": {"serious": 0, "non_serious": 0}
            }
        else:
            return {
                "success": False,
                "error": f"OpenFDA seriousness API returned status {res_serious.status_code}"
            }
            
        # 2. Get top 5 side effects (reactions)
        url_reactions = f"{url_base}?search=patient.drug.activesubstance.activesubstancename:\"{ingredient}\"&count=patient.reaction.reactionmeddrapt.exact&limit=5"
        res_reactions = requests.get(url_reactions, timeout=10)
        
        side_effects = []
        if res_reactions.status_code == 200:
            data = res_reactions.json()
            results = data.get("results", [])
            for r in results:
                side_effects.append({
                    "term": r.get("term"),
                    "count": r.get("count")
                })
                
        return {
            "success": True,
            "total_reports": total_reports,
            "side_effects": side_effects,
            "seriousness": {
                "serious": serious_count,
                "non_serious": non_serious_count
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_cache_table_if_needed(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS adverse_event_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_name TEXT UNIQUE,
        adverse_event TEXT,
        occurrence_count INTEGER,
        severity TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()

def get_adverse_events_for_ingredient(ingredient):
    """
    Get adverse event summary for a single ingredient, using SQLite cache if available and fresh.
    """
    ingredient = ingredient.upper().strip()
    if not ingredient:
        return None
        
    conn = get_db_connection()
    init_cache_table_if_needed(conn)
    cursor = conn.cursor()
    
    # 1. Check cache
    cursor.execute("""
        SELECT adverse_event, occurrence_count, severity, last_updated 
        FROM adverse_event_cache 
        WHERE ingredient_name = ?
    """, (ingredient,))
    row = cursor.fetchone()
    
    cache_fresh = False
    if row:
        last_updated_str = row['last_updated']
        try:
            last_updated = datetime.strptime(last_updated_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # Fallback if timestamp format has fractional seconds or T/Z
            last_updated_str_clean = last_updated_str.split('.')[0].replace('T', ' ').replace('Z', '')
            try:
                last_updated = datetime.strptime(last_updated_str_clean, '%Y-%m-%d %H:%M:%S')
            except Exception:
                last_updated = datetime.now() - timedelta(days=99)
                
        if datetime.now() - last_updated < timedelta(days=30):
            cache_fresh = True
            
    if cache_fresh:
        # Load from cache
        conn.close()
        return {
            "ingredient": ingredient,
            "total_reports": row['occurrence_count'],
            "side_effects": json.loads(row['adverse_event']),
            "seriousness": json.loads(row['severity']),
            "cached": True
        }
        
    # 2. Fetch new data
    print(f"Cache miss or expired for {ingredient}. Querying OpenFDA...")
    fda_data = fetch_openfda_data(ingredient)
    
    if fda_data.get("success"):
        total_reports = fda_data["total_reports"]
        side_effects = fda_data["side_effects"]
        seriousness = fda_data["seriousness"]
        
        # Save to cache
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT OR REPLACE INTO adverse_event_cache 
                (ingredient_name, adverse_event, occurrence_count, severity, last_updated)
                VALUES (?, ?, ?, ?, ?)
            """, (
                ingredient,
                json.dumps(side_effects),
                total_reports,
                json.dumps(seriousness),
                current_time
            ))
            conn.commit()
        except Exception as cache_err:
            print(f"Error saving to cache: {cache_err}")
            
        conn.close()
        return {
            "ingredient": ingredient,
            "total_reports": total_reports,
            "side_effects": side_effects,
            "seriousness": seriousness,
            "cached": False
        }
    else:
        # If API call failed but we have stale cache, fallback to stale cache
        if row:
            print(f"OpenFDA query failed for {ingredient}. Falling back to stale cache.")
            conn.close()
            return {
                "ingredient": ingredient,
                "total_reports": row['occurrence_count'],
                "side_effects": json.loads(row['adverse_event']),
                "seriousness": json.loads(row['severity']),
                "cached": True,
                "fallback": True
            }
        conn.close()
        return {
            "ingredient": ingredient,
            "total_reports": 0,
            "side_effects": [],
            "seriousness": {"serious": 0, "non_serious": 0},
            "error": fda_data.get("error")
        }

def get_product_adverse_events(ingredients_text):
    """
    Cleans and processes ingredients text, retrieves OpenFDA events for each,
    and aggregates them.
    """
    ingredients = extract_ingredients(ingredients_text)
    if not ingredients:
        return {
            "ingredients": [],
            "total_reports": 0,
            "side_effects": [],
            "seriousness": {"serious": 0, "non_serious": 0}
        }
        
    all_results = []
    total_reports = 0
    serious_total = 0
    non_serious_total = 0
    
    # Store aggregated side effects count
    reactions_map = {}
    
    for ing in ingredients:
        res = get_adverse_events_for_ingredient(ing)
        if res:
            all_results.append(res)
            total_reports += res["total_reports"]
            serious_total += res["seriousness"].get("serious", 0)
            non_serious_total += res["seriousness"].get("non_serious", 0)
            
            for se in res["side_effects"]:
                term = se["term"].upper()
                count = se["count"]
                reactions_map[term] = reactions_map.get(term, 0) + count
                
    # Sort reactions by aggregated count
    sorted_reactions = sorted(
        [{"term": term, "count": count} for term, count in reactions_map.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:5] # top 5 aggregated
    
    return {
        "ingredients": ingredients,
        "total_reports": total_reports,
        "side_effects": sorted_reactions,
        "seriousness": {
            "serious": serious_total,
            "non_serious": non_serious_total
        },
        "details": all_results
    }
