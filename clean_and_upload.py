import pandas as pd
import requests
import json

print("=" * 70)
print("MANUAL DATA CLEANING & UPLOAD")
print("=" * 70)

# Step 1: Read the messy file and find the actual data
print("\n1. Reading and cleaning Database Client file...")
file = "Schedule Ranah Creative.xlsx - Database Client (1).xlsx"

# Try different skip rows to find where actual data starts
for skip in range(0, 15):
    try:
        df = pd.read_excel(file, skiprows=skip, nrows=5)
        # Check if we found columns with actual data
        if 'Client' in str(df.columns) or 'Paket' in str(df.columns):
            print(f"   ✓ Found header at row {skip}")
            print(f"   Columns: {list(df.columns)[:10]}")
            break
        # Or check by content
        first_vals = df.iloc[0].astype(str).tolist()
        if any('client' in v.lower() or 'paket' in v.lower() or 'nama' in v.lower() for v in first_vals):
            print(f"   ✓ Found potential header at row {skip}")
            print(f"   First row: {first_vals[:5]}")
            # Use this row as header
            df = pd.read_excel(file, skiprows=skip+1)
            df.columns = pd.read_excel(file, skiprows=skip, nrows=1).iloc[0].tolist()
            break
    except:
        continue

# Read the full data with correct header
print("\n2. Loading full dataset...")
df_full = pd.read_excel(file, skiprows=skip if 'skip' in locals() else 3)
print(f"   Shape: {df_full.shape}")
print(f"   Columns: {list(df_full.columns)[:10]}")

# Show sample
print("\n3. Sample data:")
print(df_full.head(10))

# Save cleaned version
output_file = "Database_Client_CLEAN.xlsx"
df_full.to_excel(output_file, index=False)
print(f"\n4. ✓ Saved cleaned file: {output_file}")

# Upload to backend
print("\n5. Uploading to backend...")
try:
    # Upload catalog first
    with open("packages.sql", "rb") as f:
        r = requests.post("http://localhost:8000/upload-catalog", files={"file": f})
    print(f"   Catalog: {r.status_code} - {r.json().get('message')}")
    
    # Upload cleaned data
    with open(output_file, "rb") as f:
        r = requests.post("http://localhost:8000/upload", files={"file": f})
    print(f"   Data: {r.status_code}")
    result = r.json()
    print(f"   Columns detected: {result.get('columns')}")
    print(f"   Rows: {result.get('rows')}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 70)
print("NEXT: Run analysis via frontend or API")
print("=" * 70)
