import pandas as pd
import json

print("=" * 70)
print("DEBUGGING DATABASE CLIENT FILE")
print("=" * 70)

# Load the file
file = "Schedule Ranah Creative.xlsx - Database Client (1).xlsx"
print(f"\nReading file: {file}")

# Try reading with different header rows
for skip in range(0, 10):
    print(f"\n--- Trying with skiprows={skip} ---")
    try:
        df = pd.read_excel(file, skiprows=skip)
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)[:10]}")  # First 10 columns
        
        # Look for columns with keywords
        keywords = ['client', 'nama', 'paket', 'event', 'layanan', 'package']
        matching_cols = [c for c in df.columns if any(k in str(c).lower() for k in keywords)]
        
        if matching_cols:
            print(f"✓ Matching columns found: {matching_cols}")
            print(f"\nFirst 5 rows of relevant columns:")
            print(df[matching_cols].head())
            
            # Check for actual data
            non_null_count = df[matching_cols].notnull().sum().sum()
            print(f"\nNon-null values in relevant columns: {non_null_count}")
            
            if non_null_count > 10:
                print(f"\n✅ BEST HEADER ROW: {skip}")
                print(f"\nSample data:")
                for col in matching_cols[:3]:
                    unique_vals = df[col].dropna().unique()[:5]
                    print(f"  {col}: {list(unique_vals)}")
                break
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "=" * 70)
