import os
import sqlite3
import pandas as pd
from datetime import datetime

# Define paths
excel_fixed_path = '/home/galang/Documents/bpom_obat_fixed (1).xlsx'
excel_fuzzy_path = '/home/galang/Documents/bpom_obat_fuzzy_merged.xlsx'
db_path = '/home/galang/Website/waras_id.db'

def setup_database(conn):
    """Create the tables and indexes in SQLite according to database.md guidelines."""
    cursor = conn.cursor()
    
    print("Creating tables...")
    
    # 1. products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        product_name TEXT,
        registration_number TEXT,
        manufacturer TEXT,
        product_category TEXT,
        ingredient TEXT,
        atc_code TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 2. atc_reference table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS atc_reference (
        atc_code TEXT PRIMARY KEY,
        atc_name TEXT,
        ddd REAL,
        uom TEXT,
        administration_route TEXT,
        note TEXT
    );
    """)
    
    # 3. atc_hierarchy table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS atc_hierarchy (
        code TEXT PRIMARY KEY,
        name TEXT,
        level INTEGER,
        parent_code TEXT
    );
    """)
    
    # 4. adverse_event_cache table
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
    
    # 5. claim_analysis table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS claim_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        analyzed_text TEXT,
        prediction_label INTEGER,
        confidence_score REAL,
        detected_claims TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
    );
    """)
    
    # 6. product_analysis table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        claim_score REAL,
        consistency_score REAL,
        safety_score REAL,
        recommendation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
    );
    """)
    
    # Create indexes for optimal search performance
    print("Creating indexes...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_name ON products (product_name);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_reg_num ON products (registration_number);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_atc ON products (atc_code);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_ingredient ON products (ingredient);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_atc_ref_code ON atc_reference (atc_code);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_atc_hier_code ON atc_hierarchy (code);")
    
    conn.commit()
    print("Database schema setup complete.")

def process_bpom_obat(excel_path, conn):
    """Read Sheet1 from bpom_obat_fuzzy_merged.xlsx and load it into the products table."""
    print(f"Reading 'Sheet1' from {excel_path}...")
    
    # We only load the required columns to save memory and processing time
    cols_to_use = [
        'ID', 'PRODUCT_NAME', 'PRODUCT_REGISTER', 'MANUFACTURER_NAME', 
        'CATEGORY', 'INGREDIENTS', 'matched_atc_code'
    ]
    
    df = pd.read_excel(excel_path, sheet_name='Sheet1', usecols=cols_to_use)
    print(f"Loaded {len(df)} rows from fuzzy merged Excel.")
    
    # Clean data: trim strings, handle NaNs
    df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
    df = df.dropna(subset=['ID']) # ID is the primary key and must be present
    df['ID'] = df['ID'].astype(int)
    
    df['PRODUCT_NAME'] = df['PRODUCT_NAME'].fillna('').astype(str).str.strip()
    df['PRODUCT_REGISTER'] = df['PRODUCT_REGISTER'].fillna('').astype(str).str.strip()
    df['MANUFACTURER_NAME'] = df['MANUFACTURER_NAME'].fillna('').astype(str).str.strip()
    df['CATEGORY'] = df['CATEGORY'].fillna('').astype(str).str.strip()
    df['INGREDIENTS'] = df['INGREDIENTS'].fillna('').astype(str).str.strip()
    df['matched_atc_code'] = df['matched_atc_code'].fillna('').astype(str).str.strip()
    
    # Add timestamp columns
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['created_at'] = current_time
    df['updated_at'] = current_time
    
    # Rename columns to match the SQLite schema
    df_db = df.rename(columns={
        'ID': 'id',
        'PRODUCT_NAME': 'product_name',
        'PRODUCT_REGISTER': 'registration_number',
        'MANUFACTURER_NAME': 'manufacturer',
        'CATEGORY': 'product_category',
        'INGREDIENTS': 'ingredient',
        'matched_atc_code': 'atc_code'
    })
    
    # Deduplicate product IDs to prevent UNIQUE constraint failure
    print(f"Deduplicating products: {len(df_db)} rows initially...")
    df_db = df_db.drop_duplicates(subset=['id'])
    print(f"Deduplicated to {len(df_db)} unique products.")
    
    # Write to products table in SQLite
    print("Inserting data into 'products' table...")
    df_db.to_sql('products', conn, if_exists='append', index=False)
    print("Successfully populated 'products' table.")

def process_atc_ref_and_hierarchy(excel_path, conn):
    """Read WHO ATC-DDD sheet, load it into atc_reference, and build atc_hierarchy."""
    print("Reading 'WHO ATC-DDD 2026-04-25' sheet from Excel...")
    
    df = pd.read_excel(excel_path, sheet_name='WHO ATC-DDD 2026-04-25')
    print(f"Loaded {len(df)} rows from WHO ATC-DDD.")
    
    # Clean and fill NaNs
    df['atc_code'] = df['atc_code'].fillna('').astype(str).str.strip()
    df = df[df['atc_code'] != ''] # Remove any rows with empty ATC codes
    
    df['atc_name'] = df['atc_name'].fillna('').astype(str).str.strip()
    df['ddd'] = pd.to_numeric(df['ddd'], errors='coerce')
    df['uom'] = df['uom'].fillna('').astype(str).str.strip()
    df['adm_r'] = df['adm_r'].fillna('').astype(str).str.strip()
    df['note'] = df['note'].fillna('').astype(str).str.strip()
    
    # Deduplicate by atc_code
    df_ref = df.drop_duplicates(subset=['atc_code'])
    
    # Rename columns to match database schema
    df_ref_db = df_ref.rename(columns={
        'atc_code': 'atc_code',
        'atc_name': 'atc_name',
        'ddd': 'ddd',
        'uom': 'uom',
        'adm_r': 'administration_route',
        'note': 'note'
    })
    
    print("Inserting data into 'atc_reference' table...")
    df_ref_db.to_sql('atc_reference', conn, if_exists='append', index=False)
    print("Successfully populated 'atc_reference' table.")
    
    # Now build the atc_hierarchy table
    print("Building ATC hierarchy...")
    
    # Create lookup dictionary of code -> name from the excel sheet
    atc_name_map = dict(zip(df['atc_code'], df['atc_name']))
    
    hierarchy_records = []
    processed_codes = set()
    
    # Standard function to get level and parent
    def get_level_and_parent(code):
        length = len(code)
        if length == 1:
            return 1, None
        elif length == 3:
            return 2, code[0]
        elif length == 4:
            return 3, code[:3]
        elif length == 5:
            return 4, code[:4]
        elif length == 7:
            return 5, code[:5]
        else:
            if length > 5:
                return 5, code[:5]
            elif length > 4:
                return 4, code[:4]
            elif length > 3:
                return 3, code[:3]
            elif length > 1:
                return 2, code[0]
            return 1, None

    # For each ATC code, we make sure it and all its ancestors are added to the hierarchy
    for code in df_ref['atc_code']:
        # Generate ancestors
        ancestors = []
        if len(code) >= 1:
            ancestors.append(code[0])
        if len(code) >= 3:
            ancestors.append(code[:3])
        if len(code) >= 4:
            ancestors.append(code[:4])
        if len(code) >= 5:
            ancestors.append(code[:5])
        if len(code) >= 7:
            ancestors.append(code[:7])
            
        for anc in ancestors:
            if anc not in processed_codes:
                level, parent = get_level_and_parent(anc)
                # Look up name, default to uppercase code name if not in map
                name = atc_name_map.get(anc, anc)
                hierarchy_records.append({
                    'code': anc,
                    'name': name,
                    'level': level,
                    'parent_code': parent
                })
                processed_codes.add(anc)
                
    df_hier = pd.DataFrame(hierarchy_records)
    print(f"Generated {len(df_hier)} ATC hierarchy levels.")
    
    print("Inserting data into 'atc_hierarchy' table...")
    df_hier.to_sql('atc_hierarchy', conn, if_exists='append', index=False)
    print("Successfully populated 'atc_hierarchy' table.")

def main():
    if not os.path.exists(excel_fuzzy_path):
        print(f"Error: Excel file not found at {excel_fuzzy_path}")
        return
    if not os.path.exists(excel_fixed_path):
        print(f"Error: Excel file not found at {excel_fixed_path}")
        return
        
    # Remove existing database if it exists to do a clean build
    if os.path.exists(db_path):
        print(f"Removing existing database at {db_path}...")
        os.remove(db_path)
        
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)
    
    try:
        setup_database(conn)
        process_bpom_obat(excel_fuzzy_path, conn)
        process_atc_ref_and_hierarchy(excel_fixed_path, conn)
        
        # Verify sizes
        cursor = conn.cursor()
        for table in ['products', 'atc_reference', 'atc_hierarchy']:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"Table '{table}' row count: {count}")
            
        print("\nAll tasks completed successfully! The SQLite database is ready.")
        
    except Exception as e:
        import traceback
        print("\nAn error occurred during conversion:")
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
