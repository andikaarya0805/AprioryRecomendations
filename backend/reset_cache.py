import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("清理 DAN RE-UPLOAD DATA")
print("=" * 60)

# Step 1: Delete old JSON files
print("\n1. Deleting old cache files...")
import os
files_to_delete = ['rules.json', 'items.json']
for f in files_to_delete:
    if os.path.exists(f):
        os.remove(f)
        print(f"   ✓ Deleted {f}")
    else:
        print(f"   - {f} not found")

# Step 2: Re-upload catalog
print("\n2. Re-uploading catalog...")
try:
    with open("../packages.sql", "rb") as f:
        response = requests.post(f"{BASE_URL}/upload-catalog", files={"file": f})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Step 3: Check current status (should be empty)
print("\n3. Checking current status...")
try:
    response = requests.get(f"{BASE_URL}/status")
    print(f"   {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
print("SIAP UNTUK UPLOAD DATA BARU!")
print("Silakan upload file Database Client baru via frontend")
print("=" * 60)
