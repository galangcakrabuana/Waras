import pandas as pd

excel_path = '/home/galang/Documents/bpom_obat_fixed (1).xlsx'

print("Reading Excel sheets...")
xl = pd.ExcelFile(excel_path)
print("Sheet names:", xl.sheet_names)

for sheet in xl.sheet_names:
    print(f"\n--- Reading info for sheet: {sheet} ---")
    df = pd.read_excel(excel_path, sheet_name=sheet, nrows=10)
    print(f"Columns for {sheet}:")
    print(df.columns.tolist())
    print("\nFirst 2 rows:")
    print(df.head(2))
